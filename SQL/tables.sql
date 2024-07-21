CREATE TABLE zipcodeData (
    zipcode VARCHAR(10),
    medianIncome FLOAT,
    meanIncome FLOAT,
    population INT,
    PRIMARY KEY (zipcode)
);

CREATE TABLE business (
    business_id VARCHAR(50),
    name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(50),
    zipcode VARCHAR(10),
    address VARCHAR(100),
    review_count INT,
    num_checkins INT,
    stars FLOAT,
    PRIMARY KEY (business_id),
    FOREIGN KEY (zipcode) REFERENCES zipcodeData(zipcode)
);

CREATE TABLE review (
    review_id VARCHAR(50),
    review_stars FLOAT,
    date VARCHAR(10),
    text VARCHAR(1500),
    useful_vote INT,
    funny_vote INT,
    cool_vote INT,
    business_id VARCHAR(50),
    PRIMARY KEY (review_id),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE categories (
    category_name VARCHAR(50),
    business_id VARCHAR(50),
    PRIMARY KEY (category_name, business_id),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE attributes (
    attr_name VARCHAR(50),
    value VARCHAR(20),
    business_id VARCHAR(50),
    PRIMARY KEY (attr_name, business_id),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE checkins (
    day VARCHAR(20),
    time VARCHAR(20),
    count INT,
    business_id VARCHAR(50),
    PRIMARY KEY (day, time, business_id),
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);


























