UPDATE business
SET num_checkins = business_checkins_total.total_checkins
FROM (
    SELECT checkins.business_id, SUM(checkins.count) AS total_checkins
    FROM checkins
    GROUP BY checkins.business_id
) AS business_checkins_total
WHERE business.business_id = business_checkins_total.business_id;

UPDATE business
SET review_count = review_totals.num_reviews
FROM (
    SELECT review.business_id, COUNT(*) as num_reviews
    FROM review
    GROUP BY review.business_id
) AS review_totals
WHERE review_totals.business_id = business.business_id;