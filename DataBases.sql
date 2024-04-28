create table harmful_resources(
resource_id serial primary key,
resource_name varchar(200),
resource_url text,
harmful_score smallint check (harmful_score >= 1 and harmful_score <=10)
);


create table antisemitic_key_words(
word_id serial primary key,
word varchar(150),
harmful_score smallint check (harmful_score >= 1 and harmful_score <=10)
);

create table usefull_resources(
resource_id serial primary key,
resource_name varchar(200),
resource_title varchar(300),
resource_url varchar(300)
);

create table incidents(
incident_id serial primary key,
incedent_title varchar(200) not null,
incedent_info text not null,
incident_date date not null,
incident_online boolean not null
);