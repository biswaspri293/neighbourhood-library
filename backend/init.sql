---- Database: library_db
--
---- DROP DATABASE IF EXISTS library_db;
--
--CREATE DATABASE IF NOT EXISTS library;
--
--
---- Table: public.books
--
---- DROP TABLE IF EXISTS public.books;
--
--CREATE TABLE IF NOT EXISTS public.books
--(
--    id bigint NOT NULL DEFAULT nextval('books_id_seq'::regclass),
--    title character varying(255) COLLATE pg_catalog."default" NOT NULL,
--    author character varying(255) COLLATE pg_catalog."default" NOT NULL,
--    total_copies integer NOT NULL,
--    available_copies integer NOT NULL,
--    created_at timestamp without time zone DEFAULT now(),
--    CONSTRAINT books_pkey PRIMARY KEY (id),
--    CONSTRAINT unique_title_author UNIQUE (title, author),
--    CONSTRAINT books_total_copies_check CHECK (total_copies >= 0),
--    CONSTRAINT books_available_copies_check CHECK (available_copies >= 0)
--)
--
--TABLESPACE pg_default;
--
--ALTER TABLE IF EXISTS public.books
--    OWNER to postgres;
--
--
--
---- Table: public.borrowings
--
---- DROP TABLE IF EXISTS public.borrowings;
--
--CREATE TABLE IF NOT EXISTS public.borrowings
--(
--    id bigint NOT NULL DEFAULT nextval('borrowings_id_seq'::regclass),
--    member_id bigint,
--    book_id bigint,
--    borrowed_at timestamp without time zone DEFAULT now(),
--    due_date timestamp without time zone NOT NULL,
--    returned_at timestamp without time zone,
--    status character varying(20) COLLATE pg_catalog."default" DEFAULT 'BORROWED'::character varying,
--    CONSTRAINT borrowings_pkey PRIMARY KEY (id),
--    CONSTRAINT borrowings_book_id_fkey FOREIGN KEY (book_id)
--        REFERENCES public.books (id) MATCH SIMPLE
--        ON UPDATE NO ACTION
--        ON DELETE CASCADE,
--    CONSTRAINT borrowings_member_id_fkey FOREIGN KEY (member_id)
--        REFERENCES public.members (id) MATCH SIMPLE
--        ON UPDATE NO ACTION
--        ON DELETE CASCADE
--)
--
--TABLESPACE pg_default;
--
--ALTER TABLE IF EXISTS public.borrowings
--    OWNER to postgres;
---- Index: unique_active_borrow
--
---- DROP INDEX IF EXISTS public.unique_active_borrow;
--
--CREATE UNIQUE INDEX IF NOT EXISTS unique_active_borrow
--    ON public.borrowings USING btree
--    (member_id ASC NULLS LAST, book_id ASC NULLS LAST)
--    WITH (fillfactor=100, deduplicate_items=True)
--    TABLESPACE pg_default
--    WHERE status::text = 'BORROWED'::text;
--
--
--
---- Table: public.members
--
---- DROP TABLE IF EXISTS public.members;
--
--CREATE TABLE IF NOT EXISTS public.members
--(
--    id bigint NOT NULL DEFAULT nextval('members_id_seq'::regclass),
--    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
--    email character varying(255) COLLATE pg_catalog."default" NOT NULL,
--    phone character varying(20) COLLATE pg_catalog."default",
--    created_at timestamp without time zone DEFAULT now(),
--    CONSTRAINT members_pkey PRIMARY KEY (id),
--    CONSTRAINT members_email_key UNIQUE (email),
--    CONSTRAINT unique_member_email UNIQUE (email)
--)
--
--TABLESPACE pg_default;
--
--ALTER TABLE IF EXISTS public.members
--    OWNER to postgres;


-- Tables for library database
-- NOTE: Docker already creates the database using POSTGRES_DB

CREATE TABLE IF NOT EXISTS books (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    total_copies INT NOT NULL CHECK (total_copies >= 0),
    available_copies INT NOT NULL CHECK (available_copies >= 0),
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_title_author UNIQUE (title, author)
);

CREATE TABLE IF NOT EXISTS members (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS borrowings (
    id BIGSERIAL PRIMARY KEY,
    member_id BIGINT REFERENCES members(id) ON DELETE CASCADE,
    book_id BIGINT REFERENCES books(id) ON DELETE CASCADE,
    borrowed_at TIMESTAMP DEFAULT NOW(),
    due_date TIMESTAMP NOT NULL,
    returned_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'BORROWED'
);

CREATE UNIQUE INDEX IF NOT EXISTS unique_active_borrow
ON borrowings(member_id, book_id)
WHERE status = 'BORROWED';
