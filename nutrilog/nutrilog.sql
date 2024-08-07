BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"height"	REAL DEFAULT 165.0,
	"weight"	REAL DEFAULT 65.0,
	"kcal_goal"	INTEGER DEFAULT 2000,
	"water_intake_goal"	REAL DEFAULT 2.0,
	"weight_goal"	REAL DEFAULT 65.0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "food_items" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"kcal"	INTEGER,
	"protein"	REAL,
	"fat"	REAL,
	"carbohydrates"	REAL,
	"image_url"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "food_intake" (
	"id"	INTEGER NOT NULL,
	"food_item_id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"time"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"portion_weight"	REAL NOT NULL,
	"portions "	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	FOREIGN KEY("food_item_id") REFERENCES "food_items"("id")
);
CREATE TABLE IF NOT EXISTS "water_intake" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"time"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"volume"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "weight_recordings" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"time"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"weight"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);
COMMIT;
