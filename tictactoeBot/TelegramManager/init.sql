

create or replace function getRole() returns varchar as $$
DECLARE
s varchar[];
begin
s[0] = 'cross';
s[1]  = 'zero';
RETURN s[floor((random()*2))::int];
end;
$$ LANGUAGE plpgsql;


create or replace function getAnotherRole(s varchar) returns varchar as $$
begin
if s = 'cross' then return 'zero';
else  return 'cross';
end if;
end;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION generate_secret_code() returns text AS $$
DECLARE
  possible_chars TEXT := '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  output text := '';
  i integer;
  chars_size INTEGER;
  t_lenght integer = 6;
BEGIN
  chars_size := length(possible_chars);
  FOR i IN 1..t_lenght LOOP
    output := output || substr(
      possible_chars,
      (1 + FLOOR((chars_size - t_lenght + 1) * random() ))::INTEGER, 1);
  END LOOP;
  RETURN output;
END;

$$  LANGUAGE plpgsql;


create OR REPLACE FUNCTION process_games_insert() returns TRIGGER as $$
DECLARE
player_role varchar;
begin
 raise notice '%, % ', NEW.role_first_player, NEW.role_second_player;
if TG_OP = 'INSERT' then
    if NEW.role_first_player <> 'zero' then
        raise notice ' role_first_player = cross ';
        end if ;
    if NEW.role_second_player is Null then
        raise notice ' role_second_player = null ';

     end if ;
    if NEW.role_first_player is not NULL and (NEW.role_first_player <> 'cross' and NEW.role_first_player <> 'zero') then
        RAISE EXCEPTION ' role_first_player = % cannot have this value', NEW.role_first_player;

    elsif NEW.role_second_player is not  Null and (NEW.role_second_player <> 'cross' and NEW.role_second_player <> 'zero') then
        RAISE EXCEPTION 'role_second_player = % cannot have this value', NEW.role_second_player;
    end if ;

    if NEW.role_first_player is Null and NEW.role_second_player is Null then
        player_role = getRole();
        NEW.role_firts_player = getRole();
        NEW.role_second_player = getAnotherRole(player_role);


    elsif NEW.role_first_player is Null and NEW.role_second_player is not Null then
        NEW.role_first_player = getAnotherRole(NEW.role_second_player);


    elsif NEW.role_second_player is Null and NEW.role_first_player is not Null then
        NEW.role_second_player = getAnotherRole(NEW.role_first_player);

    elsif NEW.role_second_player = 'cross'  and NEW.role_first_player = 'cross' then
        NEW.role_second_player = 'zero';

         elsif NEW.role_second_player = 'zero'  and NEW.role_first_player = 'zero' then
        NEW.role_second_player = 'cross';

    end if ;


    end if ;
    return NEW;
end;
$$ LANGUAGE plpgsql;




CREATE TABLE  IF NOT EXISTS  users (
    id     integer  PRIMARY KEY
                   UNIQUE
                   NOT NULL,
    name   TEXT    NOT NULL
);

CREATE TABLE  IF NOT EXISTS  games (
    id   serial PRIMARY KEY
                 UNIQUE
                 NOT NULL,
    secret_code varchar UNIQUE NOT NUll default (generate_secret_code()),
   first_id integer references users (id) ON DELETE SET NULL,
   second_id integer references users (id) ON DELETE SET NULL,
   role_first_player varchar default (getRole()),
   role_second_player varchar default (NULL),
   status varchar NOT NUll default ('find players'),
   open_game boolean NOT NULL default(True),
   winner integer
);


CREATE TABLE  IF NOT EXISTS  boards(
    id   integer PRIMARY KEY
                 UNIQUE references games (id) ON DELETE CASCADE
                 NOT NULL,
    cross_id integer references users (id) ON DELETE CASCADE NOT NULL,
    zero_id integer references users (id) ON DELETE CASCADE NOT NULL,
   one   varchar default ('1'),
   two   varchar default ('2'),
   three varchar default ('3'),
   four  varchar default ('4'),
   five  varchar default ('5'),
   six   varchar default ('6'),
   seven varchar default ('7'),
   eight varchar default ('8'),
   nine  varchar default ('9')
);

CREATE TABLE  IF NOT EXISTS  user_and_game(
    id serial PRIMARY KEY  NOT NULL,
    user_id integer NOT NULL references users (id) ON DELETE CASCADE,
    game_id integer NOT NULL references games (id) ON DELETE CASCADE,
    status text NOT NULL default ('find players')
);



CREATE OR REPLACE FUNCTION set_game_status_starting(_id integer) returns void AS $$
BEGIN
    UPDATE games SET status = 'starting' where id = _id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_game_status_finished(_id integer) returns void AS $$
BEGIN
    UPDATE games SET status = 'finished' where id = _id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_game_status_player_joining(_id integer) returns void AS $$
BEGIN
    UPDATE games SET status = 'player joining' where id = _id;
END;
$$ LANGUAGE plpgsql;




DROP TRIGGER IF EXISTS insert_games
  ON games;

create trigger insert_games
before  insert on games
FOR each ROW
EXECUTE FUNCTION process_games_insert();


