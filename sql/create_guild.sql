

DROP TABLE IF EXISTS `guild2`;
CREATE TABLE `guild2` (
    `id` int NOT NULL AUTO_INCREMENT COMMENT 'the id of the guild',
    `name` varchar(32) NOT NULL DEFAULT '' COMMENT 'the name of the guild',
    `head` varchar(128) NOT NULL DEFAULT '' COMMENT 'the head path of the guild',
    `level` int NOT NULL DEFAULT 0 COMMENT 'the level of the guild',
    `createTime` datetime NOT NULL DEFAULT '1970-01-01 08:00:00' ,
    `createrID` int NOT NULL DEFAULT 0 COMMENT 'the creater id of the guild',
    `exp` int NOT NULL DEFAULT 0 COMMENT 'the exp of the guild',
    `province` int NOT NULL DEFAULT 0 COMMENT 'the province of the guild',
    `city` int NOT NULL DEFAULT 0 COMMENT 'the city of the guild',
    `county` int NOT NULL DEFAULT 0 COMMENT 'the county of the guild',
    `longitude` float NOT NULL DEFAULT 0 COMMENT 'the longitude of the guild',
    `latitude`  float NOT NULL DEFAULT 0 COMMENT 'the latitude of the guild',
    `limit` int NOT NULL DEFAULT 0 COMMENT 'the member limit of the guild',
    `number` int NOT NULL DEFAULT 0 COMMENT 'the member numbers of the guild',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `guildMember2`;
CREATE TABLE `guildMember2` (
    `id` int NOT NULL AUTO_INCREMENT,
    `guildID` int NOT NULL DEFAULT 0 ,
    `playerID` int NOT NULL DEFAULT 0 ,
    `playerOpenID` int NOT NULL DEFAULT 0 ,
    `exp` int NOT NULL DEFAULT 0 ,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
