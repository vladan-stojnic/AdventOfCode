use std::path;

fn read_input(path: &path::Path) -> String {
    std::fs::read_to_string(path).expect("Failed to read input file")
}

fn parse_part1(input: &str) -> (Vec<Vec<u64>>, Vec<char>) {
    let mut problems: Vec<Vec<u64>> = Vec::new();
    let mut operations: Vec<char> = Vec::new();
    for line in input.trim().lines() {
        for (i, val) in line.trim().split_whitespace().enumerate() {
            if val == "+" || val == "*" {
                operations.push(val.chars().next().unwrap());
            } else {
                if i >= problems.len() {
                    problems.push(vec![val.parse::<u64>().unwrap()]);
                } else {
                    problems[i].push(val.parse::<u64>().unwrap());
                }
            }
        }
    }
    (problems, operations)
}

fn part1(input: &str) -> u128 {
    let (problems, operations) = parse_part1(input);
    let mut total: u128 = 0;
    for (i, problem) in problems.iter().enumerate() {
        let op = operations[i];
        let result: u64 = match op {
            '+' => problem.iter().sum(),
            '*' => problem.iter().product(),
            _ => panic!("Unknown operation"),
        };
        total += result as u128;
    }
    total
}

fn parse_part2(input: &str) -> (Vec<Vec<u64>>, Vec<char>) {
    let operations: Vec<char> = input
        .trim()
        .lines()
        .last()
        .unwrap()
        .trim()
        .chars()
        .filter(|c| *c == '+' || *c == '*')
        .collect();
    let mut matrix: Vec<Vec<char>> = Vec::new();
    for line in input.lines().take(input.lines().count() - 1) {
        matrix.push(line.chars().collect());
    }
    let mut problems: Vec<Vec<u64>> = Vec::new();
    let mut is_empty = false;
    let mut problem: Vec<u64> = Vec::new();
    for col in 0..matrix[0].len() {
        let mut chars: Vec<char> = Vec::new();
        for row in 0..matrix.len() {
            let c = matrix[row][col];
            if c != ' ' {
                chars.push(c);
            }
        }
        if !chars.is_empty() {
            let num_str: String = chars.iter().collect();
            problem.push(num_str.parse::<u64>().unwrap());
        } else {
            is_empty = true;
        }
        if is_empty {
            problems.push(problem);
            problem = Vec::new();
            is_empty = false;
        }
    }
    if !problem.is_empty() {
        problems.push(problem);
    }
    (problems, operations)
}

fn part2(input: &str) -> u128 {
    let (problems, operations) = parse_part2(input);
    let mut total: u128 = 0;
    for (i, problem) in problems.iter().enumerate() {
        let op = operations[i];
        let result: u64 = match op {
            '+' => problem.iter().sum(),
            '*' => problem.iter().product(),
            _ => panic!("Unknown operation"),
        };
        total += result as u128;
    }
    total
}

fn main() {
    let input_path = path::Path::new("../data/day6.txt");
    let input = read_input(input_path);
    let result_part1 = part1(&input);
    println!("Part 1: {}", result_part1);
    let result_part2 = part2(&input);
    println!("Part 2: {}", result_part2);
}
