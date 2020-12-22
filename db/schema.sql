create table users
(
	id integer not null
		constraint users_pk
			primary key autoincrement,
	email text not null,
	password text not null
);

create unique index users_email_uindex
	on users (email);
