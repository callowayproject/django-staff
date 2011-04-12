ALTER TABLE staff_staffmember ADD COLUMN photo_height integer;
ALTER TABLE staff_staffmember ALTER COLUMN photo_height SET STORAGE PLAIN;
ALTER TABLE staff_staffmember ALTER COLUMN photo_height SET DEFAULT 0;

ALTER TABLE staff_staffmember ADD COLUMN photo_width integer;
ALTER TABLE staff_staffmember ALTER COLUMN photo_width SET STORAGE PLAIN;
ALTER TABLE staff_staffmember ALTER COLUMN photo_width SET DEFAULT 0;

ALTER TABLE staff_staffmember ADD COLUMN twitter character varying(100);
ALTER TABLE staff_staffmember ALTER COLUMN twitter SET STORAGE EXTENDED;

ALTER TABLE staff_staffmember ADD COLUMN website character varying(200);
ALTER TABLE staff_staffmember ALTER COLUMN website SET STORAGE EXTENDED;
