use std::path;

fn read_input(path: &path::Path) -> String {
    std::fs::read_to_string(path).expect("Failed to read input file")
}

fn parse_line(line: &str) -> Vec<u8> {
    line.trim()
        .chars()
        .map(|c| c.to_digit(10).unwrap() as u8)
        .collect()
}

fn parse_input(input: &str) -> Vec<Vec<u8>> {
    input.lines().map(|line| parse_line(line)).collect()
}

fn evaluate_bank(bank: &Vec<u8>, n: usize) -> u128 {
    let mut start_idx = 0;
    let mut end_idx = bank.len() - n + 1;
    let mut max_val: u128 = 0;
    for _ in 0..n {
        let (idx, m) = bank[start_idx..end_idx].iter().enumerate().fold(
            (0, 0),
            |(max_i, max_val), (idx, &val)| {
                if val > max_val {
                    (idx, val)
                } else {
                    (max_i, max_val)
                }
            },
        );
        start_idx += idx + 1;
        end_idx += 1;
        max_val = max_val * 10 + m as u128;
    }
    max_val
}

fn part1(input: &Vec<Vec<u8>>) -> u128 {
    let mut total_sum: u128 = 0;
    for bank in input {
        total_sum += evaluate_bank(bank, 2) as u128;
    }
    total_sum
}

fn part2(input: &Vec<Vec<u8>>) -> u128 {
    let mut total_sum: u128 = 0;
    for bank in input {
        total_sum += evaluate_bank(bank, 12) as u128;
    }
    total_sum
}

fn main() {
    let input_path = path::Path::new("../data/day3.txt");
    let input = read_input(input_path);
    let parsed_input = parse_input(&input);
    let result_part1 = part1(&parsed_input);
    println!("Part 1: {}", result_part1);
    let result_part2 = part2(&parsed_input);
    println!("Part 2: {}", result_part2);
}
