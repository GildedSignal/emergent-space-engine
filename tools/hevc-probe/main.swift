// HEVC complexity probe (Julien, 25 September 2026): encode a raw 8-bit luma sequence on the
// hardware HEVC encoder at fixed quality and print the bytes of every frame.
// Usage: hevc-probe <raw-luma-file> <width> <height> [quality 0..1]
import CoreMedia
import CoreVideo
import Foundation
import VideoToolbox

let args = CommandLine.arguments
guard args.count >= 4, let w = Int(args[2]), let h = Int(args[3]) else {
    FileHandle.standardError.write("usage: hevc-probe <raw-luma> <width> <height> [quality]\n".data(using: .utf8)!)
    exit(2)
}
let quality = args.count >= 5 ? Double(args[4]) ?? 0.5 : 0.5
let data = try Data(contentsOf: URL(fileURLWithPath: args[1]))
let frameBytes = w * h
let frames = data.count / frameBytes

var sizes = [Int](repeating: -1, count: frames)
var keyframes = [Bool](repeating: false, count: frames)
let lock = NSLock()

var session: VTCompressionSession?
let spec: [CFString: Any] = [kVTVideoEncoderSpecification_RequireHardwareAcceleratedVideoEncoder: true]
let status = VTCompressionSessionCreate(
    allocator: nil, width: Int32(w), height: Int32(h), codecType: kCMVideoCodecType_HEVC,
    encoderSpecification: spec as CFDictionary, imageBufferAttributes: nil, compressedDataAllocator: nil,
    outputCallback: nil, refcon: nil, compressionSessionOut: &session)
guard status == noErr, let s = session else {
    print("error: no hardware HEVC encoder (\(status))")
    exit(1)
}
VTSessionSetProperty(s, key: kVTCompressionPropertyKey_RealTime, value: kCFBooleanFalse)
VTSessionSetProperty(s, key: kVTCompressionPropertyKey_AllowFrameReordering, value: kCFBooleanFalse)
VTSessionSetProperty(s, key: kVTCompressionPropertyKey_Quality, value: quality as CFNumber)
VTSessionSetProperty(s, key: kVTCompressionPropertyKey_MaxKeyFrameInterval, value: 100000 as CFNumber)
VTCompressionSessionPrepareToEncodeFrames(s)

let start = Date()
for f in 0..<frames {
    var pb: CVPixelBuffer?
    CVPixelBufferCreate(nil, w, h, kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange, nil, &pb)
    guard let buf = pb else { exit(1) }
    CVPixelBufferLockBaseAddress(buf, [])
    let y = CVPixelBufferGetBaseAddressOfPlane(buf, 0)!.assumingMemoryBound(to: UInt8.self)
    let yStride = CVPixelBufferGetBytesPerRowOfPlane(buf, 0)
    data.withUnsafeBytes { raw in
        let src = raw.bindMemory(to: UInt8.self).baseAddress! + f * frameBytes
        for row in 0..<h {
            // Video range: map 0...255 to 16...235.
            for col in 0..<w {
                y[row * yStride + col] = UInt8(16 + Int(src[row * w + col]) * 219 / 255)
            }
        }
    }
    let uv = CVPixelBufferGetBaseAddressOfPlane(buf, 1)!.assumingMemoryBound(to: UInt8.self)
    memset(uv, 128, CVPixelBufferGetBytesPerRowOfPlane(buf, 1) * CVPixelBufferGetHeightOfPlane(buf, 1))
    CVPixelBufferUnlockBaseAddress(buf, [])
    let pts = CMTime(value: CMTimeValue(f), timescale: 30)
    VTCompressionSessionEncodeFrame(s, imageBuffer: buf, presentationTimeStamp: pts, duration: .invalid, frameProperties: nil, infoFlagsOut: nil) { st, _, sample in
        guard st == noErr, let sample = sample else { return }
        let attachments = CMSampleBufferGetSampleAttachmentsArray(sample, createIfNecessary: false) as? [[CFString: Any]]
        let notSync = (attachments?.first?[kCMSampleAttachmentKey_NotSync] as? Bool) ?? false
        lock.lock()
        sizes[f] = CMSampleBufferGetTotalSampleSize(sample)
        keyframes[f] = !notSync
        lock.unlock()
    }
}
VTCompressionSessionCompleteFrames(s, untilPresentationTimeStamp: .invalid)
let seconds = Date().timeIntervalSince(start)
for f in 0..<frames {
    print("\(f) \(sizes[f]) \(keyframes[f] ? "I" : "P")")
}
FileHandle.standardError.write("encoded \(frames) frames of \(w)x\(h) in \(String(format: "%.3f", seconds)) s\n".data(using: .utf8)!)
