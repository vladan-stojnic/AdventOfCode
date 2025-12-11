use std::collections::HashMap;
use std::path;

#[derive(Debug)]
struct Point {
    x: u64,
    y: u64,
    z: u64,
}

impl Point {
    fn distance(&self, other: &Point) -> u128 {
        (self.x as i128 - other.x as i128).pow(2) as u128
            + (self.y as i128 - other.y as i128).pow(2) as u128
            + (self.z as i128 - other.z as i128).pow(2) as u128
    }
}

fn read_input(path: &path::Path) -> String {
    std::fs::read_to_string(path).expect("Failed to read input file")
}

fn parse_line(line: &str) -> Point {
    let nums: Vec<u64> = line
        .trim()
        .split(',')
        .map(|num| num.parse::<u64>().expect("Failed to parse number"))
        .collect();
    Point {
        x: nums[0],
        y: nums[1],
        z: nums[2],
    }
}

fn parse_input(input: &str) -> Vec<Point> {
    input.lines().map(parse_line).collect()
}

fn find_all_distances(points: &Vec<Point>) -> Vec<Vec<u128>> {
    let mut distances = Vec::new();
    for i in 0..points.len() {
        let mut dists = Vec::new();
        for j in 0..points.len() {
            if i != j {
                dists.push(points[i].distance(&points[j]));
            } else {
                dists.push(u128::MAX);
            }
        }
        distances.push(dists);
    }
    distances
}

fn argmin(distances: &Vec<Vec<u128>>) -> (usize, usize) {
    let mut min_i = 0;
    let mut min_j = 0;
    let mut min_value = u128::MAX;
    for (i, row) in distances.iter().enumerate() {
        for (j, &dist) in row.iter().enumerate() {
            if dist < min_value {
                min_value = dist;
                min_i = i;
                min_j = j;
            }
        }
    }
    (min_i, min_j)
}

fn part1(junction_boxes: &Vec<Point>, num_steps: u32) -> u128 {
    let mut distances = find_all_distances(junction_boxes);
    let mut circuits: Vec<usize> = (0..junction_boxes.len()).collect();
    let mut circuit_to_junction = (0..junction_boxes.len())
        .map(|i| (i, vec![i]))
        .collect::<HashMap<usize, Vec<usize>>>();

    for _ in 0..num_steps {
        let (i, j) = argmin(&distances);
        let c1 = circuits[i];
        let c2 = circuits[j];
        let c_max = c1.max(c2);
        if c1 != c2 {
            for &junction in &circuit_to_junction[&c_max].clone() {
                circuits[junction] = c1.min(c2);
                circuit_to_junction
                    .entry(c1.min(c2))
                    .or_insert_with(Vec::new)
                    .push(junction);
            }
            circuit_to_junction.remove(&c_max);
        }
        distances[i][j] = u128::MAX;
        distances[j][i] = u128::MAX;
    }

    let mut output = circuit_to_junction
        .values()
        .map(|v| v.len())
        .collect::<Vec<usize>>();
    output.sort_by_key(|v| *v);
    output.reverse();
    output.iter().take(3).product::<usize>() as u128
}

fn part2(junction_boxes: &Vec<Point>) -> u128 {
    let mut distances = find_all_distances(junction_boxes);
    let mut circuits: Vec<usize> = (0..junction_boxes.len()).collect();
    let mut circuit_to_junction = (0..junction_boxes.len())
        .map(|i| (i, vec![i]))
        .collect::<HashMap<usize, Vec<usize>>>();

    loop {
        let (i, j) = argmin(&distances);
        let c1 = circuits[i];
        let c2 = circuits[j];
        let c_max = c1.max(c2);
        if c1 != c2 {
            for &junction in &circuit_to_junction[&c_max].clone() {
                circuits[junction] = c1.min(c2);
                circuit_to_junction
                    .entry(c1.min(c2))
                    .or_insert_with(Vec::new)
                    .push(junction);
            }
            circuit_to_junction.remove(&c_max);
        }
        distances[i][j] = u128::MAX;
        distances[j][i] = u128::MAX;
        if circuit_to_junction.len() == 1 {
            return junction_boxes[i].x as u128 * junction_boxes[j].x as u128;
        }
    }
}

fn main() {
    let input_path = path::Path::new("../data/day8.txt");
    let input = read_input(input_path);
    let junction_boxes = parse_input(&input);
    let result_part1 = part1(&junction_boxes, 1000);
    println!("Part 1 Result: {}", result_part1);
    let result_part2 = part2(&junction_boxes);
    println!("Part 2 Result: {}", result_part2);
}
