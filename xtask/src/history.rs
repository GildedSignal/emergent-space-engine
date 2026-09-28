//! Small append-only development journal. This is not the simulated event history.
use super::Result;
use std::{fs, io::Write, path::Path, process::Command};

const PATH: &str = "docs/HISTORY.md";
const FIELDS: &[&str] = &[
    "Date",
    "Kind",
    "Status",
    "Revisions",
    "Scope",
    "Changed",
    "Why",
    "Validation",
    "Evidence",
    "Limitations",
    "Next",
];

#[derive(Debug)]
struct Entry<'a> {
    number: usize,
    text: &'a str,
}

fn entries(document: &str) -> Result<Vec<Entry<'_>>> {
    let mut starts = Vec::new();
    let mut offset = 0;
    for line in document.split_inclusive('\n') {
        if line
            .strip_prefix("## H")
            .is_some_and(|s| s.starts_with(|c: char| c.is_ascii_digit()))
        {
            starts.push(offset);
        }
        offset += line.len();
    }
    let mut result = Vec::new();
    for (i, start) in starts.iter().enumerate() {
        let text = &document[*start..*starts.get(i + 1).unwrap_or(&document.len())];
        let header = text.lines().next().unwrap();
        let (id, title) = header
            .strip_prefix("## H")
            .unwrap()
            .split_once(" — ")
            .ok_or("history heading must be '## H0001 — Title'")?;
        let number: usize = id.parse()?;
        if number == 0
            || id != format!("{number:04}")
            || title.trim().is_empty()
            || title.starts_with("TODO")
        {
            return Err(format!("invalid history heading: {header}").into());
        }
        for field in FIELDS {
            let prefix = format!("- {field}: ");
            let values: Vec<_> = text
                .lines()
                .filter_map(|l| l.strip_prefix(&prefix))
                .collect();
            if values.len() != 1 || values[0].trim().is_empty() || values[0].starts_with("TODO") {
                return Err(format!("H{number:04} needs one completed {field} field").into());
            }
        }
        let date = field(text, "Date");
        if date.len() != 10
            || !date.bytes().enumerate().all(|(i, c)| {
                if i == 4 || i == 7 {
                    c == b'-'
                } else {
                    c.is_ascii_digit()
                }
            })
        {
            return Err(format!("H{number:04}: Date must be YYYY-MM-DD").into());
        }
        result.push(Entry { number, text });
    }
    if result.is_empty() {
        return Err("history contains no entries".into());
    }
    Ok(result)
}

fn field<'a>(text: &'a str, name: &str) -> &'a str {
    let prefix = format!("- {name}: ");
    text.lines()
        .find_map(|line| line.strip_prefix(&prefix))
        .unwrap_or("")
}

fn validate(document: &str, previous: Option<&str>) -> Result<usize> {
    let current = entries(document)?;
    for (i, entry) in current.iter().enumerate() {
        if entry.number != i + 1 {
            return Err("history IDs must be unique and sequential from H0001".into());
        }
    }
    if let Some(previous) = previous {
        let old = entries(previous)?;
        if old.len() > current.len()
            || old
                .iter()
                .zip(&current)
                .any(|(a, b)| a.text.trim_end() != b.text.trim_end())
        {
            return Err(
                "committed history was rewritten; append a correction entry instead".into(),
            );
        }
    }
    Ok(current.len())
}

/// Repository-relative form of a link target written relative to docs/.
fn normalize(target: &str) -> String {
    let mut parts: Vec<&str> = vec!["docs"];
    for part in target.split('/') {
        match part {
            "" | "." => {}
            ".." => {
                parts.pop();
            }
            p => parts.push(p),
        }
    }
    parts.join("/")
}

/// Evidence no longer in the working tree (docs/history-evidence-map.json): a recovered copy
/// that must exist (H0166), a path archived out of the tree that must exist in git at the
/// archive revision, an ancestor of HEAD (H0182), or a path recorded as lost for good. Any
/// other missing path still fails the check.
fn accounted(target: &str) -> Result<bool> {
    let Ok(text) = fs::read_to_string("docs/history-evidence-map.json") else { return Ok(false) };
    let map: serde_json::Value = serde_json::from_str(&text)?;
    let key = normalize(target);
    if let Some(to) = map["relocated"][&key]["to"].as_str() {
        if !Path::new(to).exists() {
            return Err(format!("relocated history evidence missing: {key} -> {to}").into());
        }
        return Ok(true);
    }
    if let Some(rev) = map["archived"]["revision"].as_str() {
        let at = |args: &[&str]| Command::new("git").args(args).output().map(|o| o.status.success()).unwrap_or(false);
        if at(&["merge-base", "--is-ancestor", rev, "HEAD"]) && at(&["cat-file", "-e", &format!("{rev}:{key}")]) {
            return Ok(true);
        }
    }
    Ok(map["lost"].get(&key).is_some())
}

fn check_links(document: &str) -> Result<()> {
    // Local Markdown evidence links are relative to docs/HISTORY.md.
    for tail in document.split("](").skip(1) {
        let Some((target, _)) = tail.split_once(')') else {
            return Err("unterminated history link".into());
        };
        let target = target
            .trim_matches(['<', '>'])
            .split('#')
            .next()
            .unwrap_or("");
        if target.is_empty() || target.contains("://") {
            continue;
        }
        if !Path::new("docs").join(target).exists() && !accounted(target)? {
            return Err(format!("missing history evidence path: {target}").into());
        }
    }
    Ok(())
}

pub fn check() -> Result<()> {
    let text = fs::read_to_string(PATH)?;
    let previous = Command::new("git")
        .args(["show", "HEAD:docs/HISTORY.md"])
        .output()?;
    let old = previous
        .status
        .success()
        .then(|| String::from_utf8_lossy(&previous.stdout).into_owned());
    let count = validate(&text, old.as_deref())?;
    check_links(&text)?;
    println!("PASS: {count} development history entries; fields, local links and committed prefix checked");
    Ok(())
}

pub fn run(args: Vec<String>) -> Result<()> {
    let action = args.first().map(String::as_str).unwrap_or("list");
    if action == "check" {
        return check();
    }
    let document = fs::read_to_string(PATH)?;
    let current = entries(&document)?;
    match action {
        "list" => {
            for entry in current {
                println!(
                    "{} | {} | {}",
                    entry.text.lines().next().unwrap().trim_start_matches("## "),
                    field(entry.text, "Date"),
                    field(entry.text, "Status")
                );
            }
        }
        "search" => {
            let needle = args
                .get(1)
                .ok_or("history search requires text")?
                .to_lowercase();
            for entry in current {
                if entry.text.to_lowercase().contains(&needle) {
                    println!("{}", entry.text.trim_end());
                }
            }
        }
        "template" => {
            let date = Command::new("date").args(["-u", "+%Y-%m-%d"]).output()?;
            if !date.status.success() {
                return Err("could not determine UTC date".into());
            }
            let date = String::from_utf8(date.stdout)?;
            println!("## H{:04} — TODO milestone title\n", current.len() + 1);
            for field in FIELDS {
                if *field == "Date" {
                    println!("- Date: {}", date.trim());
                } else {
                    println!("- {field}: TODO describe {field}");
                }
            }
        }
        "append" => {
            check()?;
            let draft =
                fs::read_to_string(args.get(1).ok_or("history append requires a draft file")?)?;
            if !draft.starts_with("## H") || entries(&draft)?.len() != 1 {
                return Err("append exactly one history entry".into());
            }
            let suffix = format!("\n\n{}\n", draft.trim_end());
            validate(&format!("{document}{suffix}"), Some(&document))?;
            check_links(&draft)?;
            // Single integrator writes; parallel agents hand their drafts to the integrator.
            let mut file = fs::OpenOptions::new().append(true).open(PATH)?;
            file.write_all(suffix.as_bytes())?;
            file.sync_all()?;
            println!("Appended history entry; commit the journal with its work.");
        }
        _ => return Err("history: list | search TEXT | template | append FILE | check".into()),
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    fn entry(n: usize) -> String {
        let mut s = format!("## H{n:04} — Actual milestone\n\n");
        for f in FIELDS {
            s += &format!(
                "- {f}: {}\n",
                if *f == "Date" {
                    "2026-09-12"
                } else {
                    "Actual recorded outcome"
                }
            );
        }
        s
    }
    #[test]
    fn completed_append_preserves_committed_records() {
        let old = entry(1);
        let new = format!("{}\n{}", old, entry(2));
        assert_eq!(validate(&new, Some(&old)).unwrap(), 2);
        let rewritten = new.replacen("Actual recorded outcome", "Different outcome", 1);
        assert!(validate(&rewritten, Some(&old)).is_err());
        assert!(validate(&old, Some(&new)).is_err());
    }
    #[test]
    fn rejects_missing_fields_duplicates_and_unfinished_templates() {
        assert!(validate(&format!("{}{}", entry(1), entry(1)), None).is_err());
        assert!(validate(
            &entry(1).replace("- Why: Actual recorded outcome\n", ""),
            None
        )
        .is_err());
        assert!(validate(
            &entry(1).replace("- Why: Actual recorded outcome", "- Why: TODO investigate"),
            None
        )
        .is_err());
    }
}
