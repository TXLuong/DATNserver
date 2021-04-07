CREATE TABLE IF NOT EXISTS Monitor(
    id bigserial NOT NULL,
    username varchar(45) NOT NULL,
    password varchar(450) NOT NULL,
    CONSTRAINT PK_Monitor PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Employee(
    id bigserial NOT NULL,
    username varchar(45) NOT NULL,
    password varchar(450) NOT NULL,
    roleId bigserial NOT NULL,
    CONSTRAINT PK_Employee PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS WorkLog(
    id bigserial NOT NULL,
    time real ,
    employeeId bigint NOT NULL,
    monitorId bigint NOT NULL,
    CONSTRAINT PK_WorkLog PRIMARY KEY (id),
    CONSTRAINT FK_WorkLog_employee FOREIGN KEY (employeeId) REFERENCES Employee(id),
    CONSTRAINT FK_WorkLog_monitor FOREIGN KEY (monitorId) REFERENCES Monitor(id)
)

-- alter table monitor 
ALTER TABLE "monitor" 
ADD column firstname varchar(45), 
ADD column lastname varchar(45),
ADD column email varchar(45)

-- alter table Employee 
ALTER TABLE "employee" 
ADD column firstname varchar(45), 
ADD column lastname varchar(45),
ADD column email varchar(45)

-- Add new table role(roleID, roleType), employee and monitor need reference it 
CREATE TABLE IF NOT EXISTS role (
    id bigserial NOT NULL,
    role varchar(50),
    CONSTRAINT pk_roleType PRIMARY KEY (id)
)

-----2-4-2021 : Update database : add accesed token  -----
alter table monitor 
add column accessedToken varchar(500)

alter table employee 
add column accessedToken varchar(500)

alter table monitor 
add column roleId bigint

alter table employee
add column roleId bigint

--- alter foreign key 
alter table monitor add constraint monitor_role_pk foreign key (roleId) references role(id)

alter table employee add constraint employee_role_pk foreign key (roleId) references role(id)