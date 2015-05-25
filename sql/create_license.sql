

DROP TABLE IF EXISTS `license`;
CREATE TABLE `license` (
    `id` int NOT NULL AUTO_INCREMENT,
    `license` varchar(8) NOT NULL DEFAULT '' COMMENT 'the license value',
    `logo` varchar(128) NOT NULL DEFAULT '' COMMENT 'the logo url',
    `name` varchar(64) NOT NULL DEFAULT '' COMMENT 'the logo name',
    `status` varchar(32) NOT NULL DEFAULT '' COMMENT 'the status of the license',
    `playerID` int NOT NULL DEFAULT 0 COMMENT 'the player id',
    `playerOpenID` varchar(64) NOT NULL DEFAULT '' COMMENT 'the player openid',
    `createTime` datetime NOT NULL DEFAULT '1970-01-01 08:00:00' ,
    `usedTime` datetime NOT NULL DEFAULT '1970-01-01 08:00:00' ,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;