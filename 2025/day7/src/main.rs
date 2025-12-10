use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::path;

fn read_input(path: &path::Path) -> String {
    std::fs::read_to_string(path).expect("Failed to read input file")
}

fn parse_input(input: &str) -> ((u64, u64), HashSet<(u64, u64)>, u64, u64) {
    let mut start: (u64, u64) = (0, 0);
    let num_lines = input.trim().lines().count();
    let num_cols = input.trim().lines().next().unwrap().trim().chars().count();
    let mut dividers: HashSet<(u64, u64)> = HashSet::new();
    for (i, line) in input.trim().lines().enumerate() {
        for (j, c) in line.trim().chars().enumerate() {
            if c == 'S' {
                start = (i as u64, j as u64);
            }
            if c == '^' {
                dividers.insert((i as u64, j as u64));
            }
        }
    }

    (start, dividers, num_lines as u64, num_cols as u64)
}

fn part1(start: (u64, u64), dividers: &HashSet<(u64, u64)>, num_lines: u64, num_cols: u64) -> u64 {
    let mut beams: VecDeque<(u64, u64)> = VecDeque::new();
    let mut visited: HashSet<(u64, u64)> = HashSet::new();
    let mut used_beams: HashSet<(u64, u64)> = HashSet::new();
    used_beams.insert(start);
    beams.push_back(start);
    while let Some((x, y)) = beams.pop_front() {
        let mut new_x = x;
        while new_x < num_lines {
            new_x += 1;
            if dividers.contains(&(new_x, y)) {
                if !visited.contains(&(new_x, y)) {
                    visited.insert((new_x, y));
                    if (y as i128 - 1) >= 0 && !used_beams.contains(&(new_x, y - 1)) {
                        beams.push_back((new_x, y - 1));
                        used_beams.insert((new_x, y - 1));
                    }
                    if y + 1 < num_cols && !used_beams.contains(&(new_x, y + 1)) {
                        beams.push_back((new_x, y + 1));
                        used_beams.insert((new_x, y + 1));
                    }
                }
                break;
            }
        }
    }

    visited.len() as u64
}

fn part2_solver(
    start: (u64, u64),
    dividers: &HashSet<(u64, u64)>,
    num_lines: u64,
    num_cols: u64,
    init_val: u64,
    memo: &mut HashMap<(u64, u64), u64>,
) -> u64 {
    if let Some(&cached) = memo.get(&start) {
        return cached + init_val;
    }
    let mut num_timelines: u64 = init_val;
    let (x, y) = start;
    let mut new_x = x;
    while new_x < num_lines {
        new_x += 1;
        if dividers.contains(&(new_x, y)) {
            if (y as i128 - 1) >= 0 {
                num_timelines +=
                    part2_solver((new_x, y - 1), dividers, num_lines, num_cols, 0, memo);
            }
            if y + 1 < num_cols {
                num_timelines +=
                    part2_solver((new_x, y + 1), dividers, num_lines, num_cols, 1, memo);
            }
            break;
        }
    }

    memo.insert(start, num_timelines - init_val);
    num_timelines
}

fn part2(start: (u64, u64), dividers: &HashSet<(u64, u64)>, num_lines: u64, num_cols: u64) -> u64 {
    let mut memo: HashMap<(u64, u64), u64> = HashMap::new();
    part2_solver(start, dividers, num_lines, num_cols, 1, &mut memo)
}

fn main() {
    let input_path = path::Path::new("../data/day7.txt");
    let input = read_input(input_path);
    let (start, dividers, num_lines, num_cols) = parse_input(&input);
    let result_part1 = part1(start, &dividers, num_lines, num_cols);
    println!("Part 1: {}", result_part1);
    let result_part2 = part2(start, &dividers, num_lines, num_cols);
    println!("Part 2: {}", result_part2);
}
