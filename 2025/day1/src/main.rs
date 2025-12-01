use std::path;

fn read_input(path: &path::Path) -> String {
    std::fs::read_to_string(path).expect("Failed to read input file")
}

fn parse_line(line: &str) -> i64 {
    if line.starts_with('R') {
        line[1..].parse::<i64>().unwrap()
    } else if line.starts_with('L') {
        -line[1..].parse::<i64>().unwrap()
    } else {
        0
    }
}

fn parse_input(input: &str) -> Vec<i64> {
    input
        .lines()
        .map(|line| parse_line(line))
        .collect::<Vec<i64>>()
}

fn part1(input: &Vec<i64>) -> u64 {
    let mut position: i64 = 50;
    let mut number_of_zeros: u64 = 0;
    for movement in input {
        position += movement;
        position = position.rem_euclid(100);
        if position == 0 {
            number_of_zeros += 1;
        }
    }
    number_of_zeros
}

fn part2(input: &Vec<i64>) -> u64 {
    let mut position: i64 = 50;
    let mut number_of_zeros: u64 = 0;
    for movement in input {
        let new_position = position + movement;
        if new_position <= 0 {
            if position > 0 {
                number_of_zeros += 1;
            }
            number_of_zeros += (new_position / 100).abs() as u64;
        } else {
            number_of_zeros += (new_position / 100) as u64;
        }
        position = new_position;
        position = position.rem_euclid(100);
    }
    number_of_zeros
}

fn main() {
    let input_path = path::Path::new("../data/day1.txt");
    let input = read_input(input_path);
    let parsed_input = parse_input(&input);
    let result_part1 = part1(&parsed_input);
    println!("Part 1: {}", result_part1);
    let result_part2 = part2(&parsed_input);
    println!("Part 2: {}", result_part2);
}
