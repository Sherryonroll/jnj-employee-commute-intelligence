# J&J Employee Commute Intelligence

This project is a data science assessment solution for estimating public transport commute attractiveness and Deutschlandticket adoption potential for synthetic employees commuting to Johnson & Johnson Medical GmbH in Norderstedt.

## Project Objective

The goal is to create a synthetic employee dataset, estimate door-to-door public transport commute times, assess commute convenience, and identify where the Deutschlandticket has strong adoption potential.

## Key Features

- Synthetic employee location generation
- Public transport accessibility estimation
- Door-to-door commute time calculation
- Commute-time grouping
- Delay sensitivity analysis using a 15-minute reliability buffer
- Walking distance to nearest station
- Number of transfers
- Deutschlandticket adoption scoring
- ML-based commuter segmentation
- Interactive map visualization
- Power BI-ready output dataset

## Project Structure

```text
notebooks/          Main notebook for the assessment
data/               Raw, synthetic, and processed datasets
src/                Python source code modules
outputs/            Charts, maps, and summary files
dashboard/          Power BI dashboard files and screenshots
```

## Main Output

The final solution will provide:

- Percentage of employees within 30, 45, 60, and over 60 minutes
- Estimated Deutschlandticket adoption potential
- Areas with strong public transport connectivity
- Areas where public transport is less attractive
- Key factors influencing adoption