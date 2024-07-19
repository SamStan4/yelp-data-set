CREATE TABLE business_classifications (
	business_id VARCHAR(50),
	successful VARCHAR(10),
	popular VARCHAR(10),
	PRIMARY KEY (business_id),
	FOREIGN KEY (business_id) REFERENCES business(business_id)
);

DROP TABLE IF EXISTS business_classifications_cpy;

CREATE TABLE business_classifications_cpy (
    SELECT * FROM business_classifications
)

INSERT INTO business_classifications_cpy(business_id, successful, popular)
SELECT business.business_id, 'false', 'false'
FROM business