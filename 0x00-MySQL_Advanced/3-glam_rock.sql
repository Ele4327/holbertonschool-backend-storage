-- Write a SQL script that lists all bands with Glam rock
-- as their main style, ranked by their longevity

/*
    Column must be in years
    You should use attributes formed and split for computing the lifespan
    Your script can be executed on any database

    Note: Output log might be outdated, (FOR SURE!)
    Make sure you use the current dates in your script
*/

SELECT band_name, ifnull(split, 2022)-ifnull(formed, 0) AS lifespan
FROM metal_bands WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
