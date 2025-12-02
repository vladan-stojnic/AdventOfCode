use std::collections::HashSet;
use std::path;

fn read_input(path: &path::Path) -> String {
    std::fs::read_to_string(path).expect("Failed to read input file")
}

fn parse_line(line: &str) -> (String, String) {
    let parts: Vec<&str> = line.split('-').collect();
    (parts[0].to_string(), parts[1].to_string())
}

fn parse_input(input: &str) -> Vec<(String, String)> {
    input.split(",").map(|line| parse_line(line)).collect()
}

fn check_range(range_start: &str, range_end: &str) -> u64 {
    let start_val = range_start.trim().parse::<u64>().unwrap();
    let end_val = range_end.trim().parse::<u64>().unwrap();
    let mut sum: u64 = 0;
    let mut start_digits = range_start[..((range_start.len() as f64) / 2.0).ceil() as usize]
        .parse::<u64>()
        .unwrap();
    let end_digits = range_end[..((range_end.len() as f64) / 2.0).ceil() as usize]
        .parse::<u64>()
        .unwrap();
    if start_digits > end_digits {
        start_digits = end_digits;
    }
    for i in start_digits..=end_digits {
        let val = i.to_string().repeat(2).parse::<u64>().unwrap();
        if val >= start_val && val <= end_val {
            sum += val;
        }
    }
    sum
}

fn part1(input: &Vec<(String, String)>) -> u64 {
    let mut total_sum: u64 = 0;
    for (range_start, range_end) in input {
        total_sum += check_range(range_start, range_end);
    }
    total_sum
}

fn divisors(num: u64) -> Vec<u64> {
    let mut divs: Vec<u64> = Vec::new();
    let mut i: u64 = 1;
    while i * i <= num {
        if num % i == 0 {
            divs.push(i);
            if i != num / i && i != 1 {
                divs.push(num / i);
            }
        }
        i += 1;
    }
    divs.sort_unstable();
    divs
}

fn check_range_2(range_start: &str, range_end: &str) -> u64 {
    let start_val = range_start.trim().parse::<u64>().unwrap();
    let end_val = range_end.trim().parse::<u64>().unwrap();
    let mut found = HashSet::new();

    let start_divisors = divisors(range_start.trim().len() as u64);
    let end_divisors = divisors(range_end.trim().len() as u64);

    let mut potential_divisors: Vec<u64> = start_divisors
        .into_iter()
        .chain(end_divisors.into_iter())
        .collect();
    potential_divisors.sort_unstable();
    potential_divisors.dedup();

    for &digit_length in &potential_divisors {
        let start = 10_u64.pow(digit_length as u32 - 1);
        let end = 10_u64.pow(digit_length as u32) - 1;
        let reps = (range_end.len() as u64) / digit_length;
        for i in start..=end {
            for rep in 2..=reps {
                let candidate = i.to_string().repeat(rep as usize).parse::<u64>().unwrap();
                if candidate >= start_val && candidate <= end_val && !found.contains(&candidate) {
                    found.insert(candidate);
                }
            }
        }
    }
    found.iter().sum()
}

fn part2(input: &Vec<(String, String)>) -> u64 {
    let mut total_sum: u64 = 0;
    for (range_start, range_end) in input {
        total_sum += check_range_2(range_start, range_end);
    }
    total_sum
}

fn main() {
    let input_path = path::Path::new("../data/day2.txt");
    let input = read_input(input_path);
    let parsed_input = parse_input(&input);
    let result_part1 = part1(&parsed_input);
    println!("Part 1: {}", result_part1);
    let result_part2 = part2(&parsed_input);
    println!("Part 2: {}", result_part2);
}
