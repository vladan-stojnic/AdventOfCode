use std::path;

fn read_input(path: &path::Path) -> String {
    std::fs::read_to_string(path).expect("Failed to read input file")
}

fn parse_input(input: &str) -> (Vec<(u128, u128)>, Vec<u128>) {
    let mut is_range = true;
    let mut ranges = vec![];
    let mut ids = vec![];
    for line in input.lines() {
        if is_range && !line.trim().is_empty() {
            let (x, y) = line.trim().split_once('-').unwrap();
            let start: u128 = x.parse().unwrap();
            let end: u128 = y.parse().unwrap();
            ranges.push((start, end));
        } else if !is_range && !line.trim().is_empty() {
            let id: u128 = line.trim().parse().unwrap();
            ids.push(id);
        } else if line.trim().is_empty() {
            // Switch mode
            is_range = false;
        }
    }
    (ranges, ids)
}

fn part1(ranges: &Vec<(u128, u128)>, ids: &Vec<u128>) -> u128 {
    let mut count = 0;
    for &id in ids {
        for &(start, end) in ranges {
            if id >= start && id <= end {
                count += 1;
                break;
            }
        }
    }
    count
}

fn merge_ranges(ranges: &Vec<(u128, u128)>) -> Vec<(u128, u128)> {
    let mut sorted_ranges = ranges.clone();
    sorted_ranges.sort_by_key(|r| r.0);
    let mut merged = vec![];
    let mut current_start = sorted_ranges[0].0;
    let mut current_end = sorted_ranges[0].1;

    for &(start, end) in &sorted_ranges[1..] {
        if start <= current_end + 1 {
            current_end = current_end.max(end);
        } else {
            merged.push((current_start, current_end));
            current_start = start;
            current_end = end;
        }
    }
    merged.push((current_start, current_end));
    merged
}

fn part2(ranges: &Vec<(u128, u128)>) -> u128 {
    let merged_ranges = merge_ranges(ranges);
    let mut count = 0;
    for &(start, end) in &merged_ranges {
        count += end - start + 1;
    }
    count
}

fn main() {
    let input_path = path::Path::new("../data/day5.txt");
    let input = read_input(input_path);
    let (ranges, ids) = parse_input(&input);
    let result_part1 = part1(&ranges, &ids);
    println!("Part 1: {}", result_part1);
    let result_part2 = part2(&ranges);
    println!("Part 2: {}", result_part2);
}
