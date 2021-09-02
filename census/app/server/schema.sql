DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

SET timezone TO 'Europe/Warsaw';



CREATE TABLE users(
  id SERIAL PRIMARY KEY,
  name VARCHAR(45) NOT NULL,
  second_name VARCHAR(45) NULL,
  last_name VARCHAR(45) NOT NULL,
  birth_date DATE NULL,
  picture bytea NULL,
  password VARCHAR(255) NOT NULL,
  privilage_level INTEGER NULL
);

CREATE TABLE mail(
  id SERIAL PRIMARY KEY,
  address VARCHAR(255) NOT NULL UNIQUE,
  user_id INTEGER REFERENCES users(id)
);

ALTER TABLE users ADD primary_mail_id INTEGER REFERENCES mail(id) NULL;

CREATE TYPE platforms AS ENUM('github', 'gitlab', 'bitbucket', 'facebook', 'twitter', 'linkedin', 'google', 'youtube', 'other');
CREATE TABLE social (
  id INT NOT NULL,
  name VARCHAR(200) NULL,
  platform platforms NULL,
  description TEXT NULL,
  user_id INT NOT NULL
);

CREATE TABLE school(
  id SERIAL PRIMARY KEY,
  name VARCHAR(45) NOT NULL
);

CREATE TABLE department (
  id SERIAL PRIMARY KEY,
  name VARCHAR(45) NULL,
  school_id INTEGER REFERENCES school(id)
);
CREATE TYPE available_degrees AS ENUM('inżynierskie', 'licencjackie', 'magisterskie', 'magisterskie jednolite');
CREATE TABLE classes(
  id SERIAL PRIMARY KEY,
  department_id INTEGER REFERENCES department(id),
  name VARCHAR(45) NULL,
  degree available_degrees NULL
);

CREATE TABLE user_has_classes (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  classes_id INT NOT NULL,
  semester INT NULL
);