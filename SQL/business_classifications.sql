CREATE TABLE classifications AS
WITH business_scores AS (
    SELECT 
        business.business_id, 
        business.zipcode, 
        business.num_checkins, 
        (
            CASE WHEN business.num_checkins = 0 THEN 0 ELSE LOG(business.num_checkins) END +
            CASE WHEN business.review_count = 0 THEN 0 ELSE LOG(business.review_count) END +
            CASE WHEN business.stars = 0 THEN 0 ELSE LOG(business.stars) END
        ) AS successful_score
    FROM business
),
zipcode_score_averages AS (
    SELECT 
        zipcode_totals.zipcode, 
        AVG(zipcode_totals.successful_score) AS successful_score_avg, 
        AVG(zipcode_totals.num_checkins) AS num_checkins_avg
    FROM (
        SELECT 
            business.zipcode, 
            business.num_checkins, 
            (
                CASE WHEN business.num_checkins = 0 THEN 0 ELSE LOG(business.num_checkins) END +
                CASE WHEN business.review_count = 0 THEN 0 ELSE LOG(business.review_count) END +
                CASE WHEN business.stars = 0 THEN 0 ELSE LOG(business.stars) END
            ) AS successful_score
        FROM business
    ) AS zipcode_totals
    GROUP BY zipcode_totals.zipcode
)
SELECT business_scores.business_id, (
		CASE WHEN business_scores.num_checkins > zipcode_score_averages.num_checkins_avg
		THEN 'true' ELSE 'false' END
	) AS popular, (
		CASE WHEN business_scores.successful_score > zipcode_score_averages.successful_score_avg
		THEN 'true' ELSE 'false' END
	) AS successful
FROM business_scores INNER JOIN zipcode_score_averages 
ON business_scores.zipcode = zipcode_score_averages.zipcode; 