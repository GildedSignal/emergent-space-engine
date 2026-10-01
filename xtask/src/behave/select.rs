//! The arguments of `behave`: `--law NAME` and `--gates ID[,ID...]`, each also as `--flag=value`,
//! in any order. Gate ids are case-insensitive. No `--gates` means every gate.

/// Every gate the judge runs, in the order it runs them. B8 (determinism) is an engine test, not a behaviour.
pub const ALL: [&str; 16] = ["G1", "G2", "G3", "G4", "G5", "G6", "B7", "B9", "B10", "B11", "B12", "B13", "B14", "B16", "B17", "B18"];
/// The gates of the single mass (the first nine): what `judge` runs. B11-B14 judge the events layer;
/// B16-B18 are the red-team's (moving lenses, resonance, memory).
pub const CORE: [&str; 9] = ["G1", "G2", "G3", "G4", "G5", "G6", "B7", "B9", "B10"];

#[derive(Debug, PartialEq)]
pub struct Args {
    pub law: String,
    /// None: every gate.
    pub gates: Option<Vec<&'static str>>,
}

fn gate(id: &str) -> Result<&'static str, String> {
    let id = id.to_ascii_uppercase();
    match ALL.iter().find(|g| **g == id) {
        Some(g) => Ok(g),
        None if id == "B8" => Err("B8 is judged by the engine tests, not by behave".into()),
        None => Err(format!("unknown gate {id:?}")),
    }
}

/// Parses the arguments after `behave`.
pub fn parse(args: &[String]) -> Result<Args, String> {
    let (mut law, mut gates) = (None, None);
    let mut it = args.iter();
    while let Some(arg) = it.next() {
        let (flag, inline) = match arg.split_once('=') {
            Some((f, v)) => (f, Some(v.to_string())),
            None => (arg.as_str(), None),
        };
        let value = |it: &mut std::slice::Iter<String>| inline.clone().or_else(|| it.next().cloned()).ok_or(format!("{flag} needs a value"));
        match flag {
            "--law" if law.is_none() => law = Some(value(&mut it)?),
            "--gates" if gates.is_none() => {
                let mut ids: Vec<&'static str> = Vec::new();
                for id in value(&mut it)?.split(',') {
                    let g = gate(id)?;
                    if !ids.contains(&g) {
                        ids.push(g);
                    }
                }
                gates = Some(ids);
            }
            "--law" | "--gates" => return Err(format!("{flag} given twice")),
            _ => return Err(format!("unknown argument {arg:?}")),
        }
    }
    // Gates run in the judge's order, whatever order they were named in.
    let gates = gates.map(|ids| ALL.iter().copied().filter(|g| ids.contains(g)).collect());
    Ok(Args { law: law.unwrap_or_else(|| "echo".into()), gates })
}

#[cfg(test)]
mod tests {
    use super::*;

    fn parse_all(args: &[&str]) -> Result<Args, String> {
        parse(&args.iter().map(|a| a.to_string()).collect::<Vec<_>>())
    }

    #[test]
    fn the_default_is_echo_and_every_gate() {
        assert_eq!(parse_all(&[]), Ok(Args { law: "echo".into(), gates: None }));
    }

    #[test]
    fn law_and_gates_in_either_spelling_and_order() {
        let want = Ok(Args { law: "planted-clock".into(), gates: Some(vec!["B7", "B9"]) });
        assert_eq!(parse_all(&["--law", "planted-clock", "--gates", "B7,B9"]), want);
        assert_eq!(parse_all(&["--gates=b9,B7", "--law=planted-clock"]), want);
        assert_eq!(parse_all(&["--gates", "B10,g1,B10"]), Ok(Args { law: "echo".into(), gates: Some(vec!["G1", "B10"]) }));
    }

    #[test]
    fn bad_gates_and_arguments_are_refused() {
        for args in [&["--gates", "B8"][..], &["--gates", "G7"], &["--gates", ""], &["--gates", "B7,"], &["--gates"], &["--law"], &["--fast"], &["--law", "a", "--law", "b"], &["B7"]] {
            assert!(parse_all(args).is_err(), "{args:?}");
        }
        assert!(parse_all(&["--gates", "B8"]).unwrap_err().contains("engine tests"));
    }

    #[test]
    fn the_events_gates_are_named_in_the_judges_order_and_the_core_is_the_first_nine() {
        assert_eq!(parse_all(&["--gates", "b14,B11,B13"]), Ok(Args { law: "echo".into(), gates: Some(vec!["B11", "B13", "B14"]) }));
        assert_eq!(parse_all(&["--gates", "b18,B16,B9,b17"]), Ok(Args { law: "echo".into(), gates: Some(vec!["B9", "B16", "B17", "B18"]) }));
        assert_eq!(CORE[..], ALL[..9]);
        assert_eq!(ALL[9..], ["B11", "B12", "B13", "B14", "B16", "B17", "B18"]);
        assert!(parse_all(&["--law", "planted-kick"]).is_ok());
    }
}
