use std::path;

fn read_input(path: &path::Path) -> String {
    std::fs::read_to_string(path).expect("Failed to read input file")
}

fn parse_line(line: &str) -> Vec<char> {
    line.trim().chars().collect()
}

fn parse_input(input: &str) -> Vec<Vec<char>> {
    input.lines().map(|line| parse_line(line)).collect()
}

fn evaluate_location(grid: &Vec<Vec<char>>, row: usize, col: usize) -> bool {
    let mut occupied_count = 0;
    for i in -1..=1 {
        for j in -1..=1 {
            if i == 0 && j == 0 {
                continue;
            }
            let new_row = row as isize + i;
            let new_col = col as isize + j;
            if new_row >= 0
                && new_row < grid.len() as isize
                && new_col >= 0
                && new_col < grid[0].len() as isize
            {
                if grid[new_row as usize][new_col as usize] == '@' {
                    occupied_count += 1;
                }
            }
        }
    }
    occupied_count < 4
}

fn part1(input: &Vec<Vec<char>>) -> (u64, Vec<Vec<char>>) {
    let mut movable: u64 = 0;
    let mut input_clone = input.clone();
    for (row_idx, row) in input.iter().enumerate() {
        for (col_idx, _) in row.iter().enumerate() {
            if evaluate_location(input, row_idx, col_idx) && input[row_idx][col_idx] == '@' {
                movable += 1;
                input_clone[row_idx][col_idx] = 'x';
            }
        }
    }
    (movable, input_clone)
}

fn part2(input: &Vec<Vec<char>>) -> u64 {
    let mut total_movable: u64 = 0;
    let mut current_grid = input.clone();
    loop {
        let (movable, new_grid) = part1(&current_grid);
        if movable == 0 {
            break;
        }
        total_movable += movable;
        current_grid = new_grid;
    }
    total_movable
}

fn main() {
    let input_path = path::Path::new("../data/day4.txt");
    let input = read_input(input_path);
    let parsed_input = parse_input(&input);
    let (result_part1, _) = part1(&parsed_input);
    println!("Part 1: {}", result_part1);
    let result_part2 = part2(&parsed_input);
    println!("Part 2: {}", result_part2);
}
