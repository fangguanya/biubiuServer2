
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player2` (
  `id` int(11) NOT NULL DEFAULT '0',
  `gold` bigint(20) NOT NULL DEFAULT '0',
  `diamond` bigint(20) NOT NULL DEFAULT '0',
  `level` int(11) NOT NULL DEFAULT '1',
  `intelligence` int(11) NOT NULL DEFAULT '0',
  `rmb` int(11) NOT NULL DEFAULT '0',
  `exp` int(11) NOT NULL DEFAULT '0',
  `sex` int(11) NOT NULL DEFAULT '0',
  `vip` int(11) NOT NULL DEFAULT '0',
  `vigor` int(11) NOT NULL DEFAULT '0',
  `title` int(11) NOT NULL DEFAULT '0',
  `item1` int(11) NOT NULL DEFAULT '0',
  `item2` int(11) NOT NULL DEFAULT '0',
  `item3` int(11) NOT NULL DEFAULT '0',
  `item4` int(11) NOT NULL DEFAULT '0',
  `item5` int(11) NOT NULL DEFAULT '0',
  `loginReward` int(11) NOT NULL DEFAULT '0',
  `firstRechargeReward` tinyint(4) NOT NULL DEFAULT '0',
  `levelReward` int(11) NOT NULL DEFAULT '0',
  `rank` smallint(6) NOT NULL DEFAULT '0',
  `bestRank` smallint(6) NOT NULL DEFAULT '0',
  `achievement` bigint(20) NOT NULL DEFAULT '0',
  `contribution` bigint(20) NOT NULL DEFAULT '0',
  `allScore` bigint(20) NOT NULL DEFAULT '0',
  `success` bigint(20) NOT NULL DEFAULT '0',
  `failure` bigint(20) NOT NULL DEFAULT '0',
  `honor` bigint(20) NOT NULL DEFAULT '0',
  `nextFreeDrawTime` datetime NOT NULL DEFAULT '1970-01-01 08:00:00',
  `nextPvpOnlineTime` datetime NOT NULL DEFAULT '1970-01-01 08:00:00',
  `login` datetime NOT NULL DEFAULT '1970-01-01 08:00:00',
  `logout` datetime NOT NULL DEFAULT '1970-01-01 08:00:00',
  `vigorTime` datetime NOT NULL DEFAULT '1970-01-01 08:00:00',
  `pvpOfflineCooldown` datetime NOT NULL DEFAULT '1970-01-01 08:00:00',
  `pvpCandidateCooldown` datetime NOT NULL DEFAULT '1970-01-01 08:00:00',
  `account` varchar(32) NOT NULL DEFAULT '',
  `name` varchar(32) NOT NULL DEFAULT '',
  `accountID` int(11) NOT NULL DEFAULT '0',
  `guid` varchar(36) NOT NULL DEFAULT '',
  `create_server_id` int(11) NOT NULL DEFAULT '-1',
  `current_server_id` int(11) NOT NULL DEFAULT '-1',
  `allScore1` bigint(20) NOT NULL DEFAULT '0',
  `allScore2` bigint(20) NOT NULL DEFAULT '0',
  `allScore3` bigint(20) NOT NULL DEFAULT '0',
  `allScore4` bigint(20) NOT NULL DEFAULT '0',
  `agency` int(11) NOT NULL DEFAULT '0',
  `nameBrand` int(11) NOT NULL DEFAULT '0',
  `qq` varchar(32) NOT NULL DEFAULT '',
  `guild` int(11) NOT NULL DEFAULT '0',
  `headurl` varchar(128) NOT NULL DEFAULT '',
  `guildId` int(11) NOT NULL DEFAULT '0',
  `gem` int(11) NOT NULL DEFAULT '0',
  `prop` varchar(128) NOT NULL DEFAULT '{}',
  `inviter` int(11) NOT NULL DEFAULT '0',
  `modify_cnt` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
