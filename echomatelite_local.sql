-- MySQL dump 10.13  Distrib 9.6.0, for macos26.4 (arm64)
--
-- Host: localhost    Database: echomatelite
-- ------------------------------------------------------
-- Server version	9.6.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'd71c1300-68f2-11f1-b8de-8f7dc35c8277:1-1859';

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `comment` text NOT NULL,
  `user_id` int DEFAULT NULL,
  `post_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (1,'faboulous',1,7,'2026-06-19 09:30:25'),(2,'faboulous',1,7,'2026-06-19 09:30:29'),(3,'faboulous',1,7,'2026-06-19 09:30:38'),(4,'hey good morning',1,7,'2026-06-19 09:30:46'),(5,'qwerty',1,7,'2026-06-19 09:31:02'),(6,'qwerty',1,7,'2026-06-19 09:34:02'),(7,'nice pic bro',1,6,'2026-06-19 09:37:19'),(8,'faboulous',1,8,'2026-06-20 07:05:03'),(9,'faboulous',1,11,'2026-06-20 13:53:54'),(17,'faboulous',10,45,'2026-07-09 17:49:06'),(43,'fantastic bro',1,30,'2026-07-14 21:14:15'),(61,'wd',1,35,'2026-07-15 05:52:24'),(63,'fantastic bro',1,49,'2026-07-15 06:38:44'),(94,'12',1,45,'2026-07-22 05:47:25'),(96,'3r2',1,55,'2026-07-22 05:49:41');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `followers`
--

DROP TABLE IF EXISTS `followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `followers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `follower_id` int DEFAULT NULL,
  `following_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `followers`
--

LOCK TABLES `followers` WRITE;
/*!40000 ALTER TABLE `followers` DISABLE KEYS */;
INSERT INTO `followers` VALUES (3,4,1),(9,2,1),(14,10,2),(15,10,1),(19,2,10),(21,1,9),(23,1,2),(24,1,4);
/*!40000 ALTER TABLE `followers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `likes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `post_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=262 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES (1,1,4),(2,1,4),(3,1,4),(4,1,3),(5,1,3),(6,1,4),(7,1,3),(8,1,4),(9,1,4),(10,1,4),(11,1,4),(12,1,4),(13,1,4),(14,1,3),(15,1,3),(16,1,3),(17,1,3),(18,1,5),(19,1,7),(20,1,7),(21,1,7),(30,4,6),(31,4,3),(37,1,8),(38,2,9),(39,1,10),(41,1,11),(60,10,11),(61,10,12),(62,10,41),(63,10,40),(78,1,39),(82,1,42),(86,1,38),(88,1,37),(91,1,34),(104,1,40),(113,1,48),(114,1,35),(117,1,49),(120,2,45),(122,2,12),(123,1,51),(164,1,50),(188,2,50),(194,10,52),(222,10,50),(246,1,45),(249,1,53),(253,1,52),(255,1,55),(256,2,57),(257,2,55),(258,2,53),(261,1,57);
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (5,2,2,'hey dude what\'s going on','2026-06-21 07:45:41'),(6,2,2,'hey i am good you tell','2026-06-21 07:45:54'),(7,9,2,'Hey','2026-06-24 17:30:34'),(8,10,2,'hii','2026-07-04 11:06:51'),(12,2,2,'Bdhia','2026-07-15 07:46:28'),(15,1,10,'🔗 Hey! Check out this post: /feed#post45','2026-07-20 07:45:04'),(16,1,10,'POST_SHARE:50','2026-07-20 07:54:27'),(17,1,10,'POST_SHARE:53','2026-07-20 08:34:34'),(19,1,9,'POST_SHARE:55','2026-07-20 09:35:05'),(20,1,9,'POST_SHARE:12','2026-07-20 17:01:45'),(21,1,9,'POST_SHARE:50','2026-07-20 17:03:43'),(24,2,1,'POST_SHARE:55','2026-07-21 14:24:24'),(25,2,9,'Wassup ','2026-07-21 14:53:46'),(27,10,1,'POST_SHARE:57','2026-07-21 19:50:49'),(34,10,2,'Hy','2026-07-21 20:29:36'),(35,10,1,'POST_SHARE:53','2026-07-21 20:38:36'),(37,10,1,'POST_SHARE:52','2026-07-21 21:04:51'),(38,10,2,'POST_SHARE:45','2026-07-21 21:05:45'),(39,1,2,'POST_SHARE:45','2026-07-22 05:47:31'),(40,1,2,'POST_SHARE:55','2026-07-22 05:48:55'),(41,1,5,'POST_SHARE:57','2026-07-22 06:00:36'),(42,2,1,'POST_SHARE:50','2026-07-22 06:07:40');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `message` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `target_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=143 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,1,'Ali followed you','2026-06-19 19:46:03',NULL),(2,1,'Ali followed you','2026-06-20 07:02:30',NULL),(3,4,'tahoor followed you','2026-06-20 07:03:48',NULL),(4,2,'tahoor commented on your post','2026-06-20 07:05:03',NULL),(5,2,'tahoor liked your post','2026-06-20 07:05:18',NULL),(6,2,'tahoor liked your post','2026-06-20 08:18:06',NULL),(7,1,'Ali followed you','2026-06-20 09:46:23',NULL),(8,2,'You received a new message','2026-06-21 07:45:41',NULL),(9,2,'You received a new message','2026-06-21 07:45:54',NULL),(10,2,'tahoor followed you','2026-06-21 08:05:09',NULL),(11,2,'tahoor followed you','2026-06-21 08:05:12',NULL),(12,2,'ahsan followed you','2026-06-24 17:30:24',NULL),(13,2,'ahsan followed you','2026-06-24 17:30:29',NULL),(14,2,'You received a new message','2026-06-24 17:30:34',NULL),(15,2,'shihaab followed you','2026-07-04 11:06:43',NULL),(16,2,'You received a new message','2026-07-04 11:06:51',NULL),(17,2,'shihaab liked your post','2026-07-08 14:28:55',NULL),(18,2,'shihaab liked your post','2026-07-08 15:20:58',NULL),(19,2,'shihaab commented on your post','2026-07-09 09:24:17',NULL),(20,2,'shihaab liked your post','2026-07-09 14:19:42',NULL),(21,2,'shihaab liked your post','2026-07-09 14:19:48',NULL),(22,2,'shihaab liked your post','2026-07-09 16:46:19',NULL),(23,2,'shihaab liked your post','2026-07-09 16:47:23',NULL),(24,1,'shihaab followed you','2026-07-09 16:47:44',NULL),(25,1,'shihaab liked your post','2026-07-09 16:47:56',NULL),(26,2,'shihaab liked your post','2026-07-09 16:47:59',NULL),(27,1,'shihaab liked your post','2026-07-09 16:48:05',NULL),(28,1,'shihaab liked your post','2026-07-09 16:48:07',NULL),(29,1,'shihaab commented on your post','2026-07-09 16:53:39',NULL),(30,2,'You received a new message','2026-07-12 07:05:11',NULL),(31,2,'tahoor liked your post','2026-07-12 07:13:37',NULL),(32,1,'You received a new message','2026-07-15 05:49:58',NULL),(33,1,'You received a new message','2026-07-15 05:50:02',NULL),(34,2,'tahoor liked your post','2026-07-15 06:14:50',NULL),(35,2,'tahoor followed you','2026-07-15 06:15:16',NULL),(36,2,'tahoor followed you','2026-07-15 06:15:17',NULL),(37,2,'tahoor followed you','2026-07-15 06:15:27',NULL),(38,2,'You received a new message','2026-07-15 07:46:28',NULL),(39,9,'You received a new message','2026-07-15 07:46:35',NULL),(40,10,'Ali followed you','2026-07-15 07:46:48',NULL),(41,10,'Ali liked your post','2026-07-15 07:47:02',NULL),(42,1,'Ali liked your post','2026-07-15 07:47:09',NULL),(43,10,'tahoor followed you','2026-07-15 08:20:05',NULL),(44,10,'tahoor commented on your post','2026-07-15 12:31:23',NULL),(45,9,'tahoor followed you','2026-07-15 13:16:41',NULL),(46,10,'tahoor liked your post','2026-07-15 13:32:31','/feed#post45'),(47,10,'tahoor shared a post with you','2026-07-20 07:44:58','/chat/1'),(48,10,'tahoor shared a post with you','2026-07-20 07:45:04','/chat/1'),(49,10,'tahoor shared a post with you','2026-07-20 07:54:27','/chat/1'),(50,10,'tahoor shared a post with you','2026-07-20 08:34:34','/chat/1'),(51,10,'You received a new message','2026-07-20 08:34:57','/chat/1'),(52,10,'tahoor followed you','2026-07-20 08:44:33','/user/1'),(53,9,'tahoor shared a post with you','2026-07-20 09:35:05','/chat/1'),(54,2,'tahoor followed you','2026-07-20 11:28:20','/user/1'),(55,4,'tahoor followed you','2026-07-20 11:28:28','/user/1'),(56,2,'tahoor liked your post','2026-07-20 15:41:41','/feed#post12'),(57,2,'tahoor liked your post','2026-07-20 15:41:42','/feed#post12'),(58,2,'tahoor liked your post','2026-07-20 16:00:32','/feed#post12'),(59,9,'tahoor shared a post with you','2026-07-20 17:01:45','/chat/1'),(60,9,'tahoor shared a post with you','2026-07-20 17:03:43','/chat/1'),(61,2,'You received a new message','2026-07-21 12:08:42','/chat/1'),(62,2,'You received a new message','2026-07-21 12:42:57','/chat/1'),(63,1,'Ali liked your post','2026-07-21 14:22:38','/feed#post55'),(64,1,'Ali liked your post','2026-07-21 14:24:13','/feed#post55'),(65,1,'Ali commented on your post','2026-07-21 14:24:20','/feed#post55'),(66,1,'Ali shared a post with you','2026-07-21 14:24:24','/chat/2'),(67,1,'Ali liked your post','2026-07-21 14:46:34','/feed#post55'),(68,9,'You received a new message','2026-07-21 14:53:46','/chat/2'),(69,1,'Ali liked your post','2026-07-21 15:49:34','/feed#post53'),(70,9,'Ali followed you','2026-07-21 15:49:52','/user/2'),(71,1,'Ali liked your post','2026-07-21 18:03:33','/feed#post55'),(72,1,'Ali commented on your post','2026-07-21 18:17:32','/feed#post55'),(73,1,'Ali commented on your post','2026-07-21 18:26:01','/feed#post55'),(74,1,'Ali commented on your post','2026-07-21 18:33:02','/feed#post50'),(75,1,'Ali commented on your post','2026-07-21 18:33:04','/feed#post50'),(76,2,'shihaab commented on your post','2026-07-21 19:41:24','/feed#post57'),(77,2,'shihaab commented on your post','2026-07-21 19:43:35','/feed#post57'),(78,1,'You received a new message','2026-07-21 19:43:57','/chat/10'),(79,1,'shihaab shared a post with you','2026-07-21 19:50:49','/chat/10'),(80,1,'shihaab shared a post with you','2026-07-21 19:54:04','/chat/10'),(81,1,'shihaab commented on your post','2026-07-21 19:54:45','/feed#post55'),(82,1,'shihaab commented on your post','2026-07-21 20:06:45','/feed#post55'),(83,1,'shihaab commented on your post','2026-07-21 20:07:05','/feed#post55'),(84,1,'shihaab shared a post with you','2026-07-21 20:16:07','/chat/10'),(85,1,'shihaab shared a post with you','2026-07-21 20:16:44','/chat/10'),(86,2,'shihaab shared a post with you','2026-07-21 20:16:46','/chat/10'),(87,1,'shihaab shared a post with you','2026-07-21 20:28:00','/chat/10'),(88,2,'shihaab shared a post with you','2026-07-21 20:28:51','/chat/10'),(89,2,'You received a new message','2026-07-21 20:29:36','/chat/10'),(90,1,'shihaab shared a post with you','2026-07-21 20:38:36','/chat/10'),(91,2,'shihaab commented on your post','2026-07-21 20:51:09','/feed#post57'),(92,2,'shihaab liked your post','2026-07-21 20:54:40','/feed#post57'),(93,2,'shihaab liked your post','2026-07-21 20:54:42','/feed#post57'),(94,2,'shihaab liked your post','2026-07-21 20:54:43','/feed#post57'),(95,2,'shihaab liked your post','2026-07-21 20:54:44','/feed#post57'),(96,2,'shihaab liked your post','2026-07-21 20:54:45','/feed#post57'),(97,2,'shihaab liked your post','2026-07-21 20:54:47','/feed#post57'),(98,2,'shihaab liked your post','2026-07-21 20:54:51','/feed#post57'),(99,2,'shihaab liked your post','2026-07-21 20:55:36','/feed#post57'),(100,2,'shihaab liked your post','2026-07-21 20:55:37','/feed#post57'),(101,2,'shihaab liked your post','2026-07-21 20:55:38','/feed#post57'),(102,1,'shihaab liked your post','2026-07-21 20:55:55','/feed#post55'),(103,1,'shihaab liked your post','2026-07-21 20:55:56','/feed#post55'),(104,1,'shihaab liked your post','2026-07-21 20:56:59','/feed#post55'),(105,1,'shihaab liked your post','2026-07-21 20:57:00','/feed#post55'),(106,1,'shihaab liked your post','2026-07-21 20:57:01','/feed#post55'),(107,1,'shihaab liked your post','2026-07-21 20:57:02','/feed#post55'),(108,1,'shihaab liked your post','2026-07-21 20:57:05','/feed#post53'),(109,1,'shihaab liked your post','2026-07-21 20:58:38','/feed#post55'),(110,1,'shihaab liked your post','2026-07-21 21:00:30','/feed#post55'),(111,1,'shihaab liked your post','2026-07-21 21:00:39','/feed#post50'),(112,1,'shihaab liked your post','2026-07-21 21:01:38','/feed#post55'),(113,1,'shihaab liked your post','2026-07-21 21:01:39','/feed#post55'),(114,1,'shihaab liked your post','2026-07-21 21:01:40','/feed#post55'),(115,1,'shihaab commented on your post','2026-07-21 21:01:43','/feed#post55'),(116,1,'shihaab shared a post with you','2026-07-21 21:01:47','/chat/10'),(117,1,'shihaab liked your post','2026-07-21 21:04:40','/feed#post55'),(118,1,'shihaab liked your post','2026-07-21 21:04:42','/feed#post55'),(119,1,'shihaab liked your post','2026-07-21 21:04:46','/feed#post53'),(120,1,'shihaab shared a post with you','2026-07-21 21:04:51','/chat/10'),(121,2,'shihaab shared a post with you','2026-07-21 21:05:45','/chat/10'),(122,1,'shihaab liked your post','2026-07-21 21:06:33','/feed#post55'),(123,2,'tahoor liked your post','2026-07-22 05:39:59','/feed#post57'),(124,2,'tahoor liked your post','2026-07-22 05:40:01','/feed#post57'),(125,2,'tahoor liked your post','2026-07-22 05:40:02','/feed#post57'),(126,2,'tahoor liked your post','2026-07-22 05:40:24','/feed#post57'),(127,10,'tahoor liked your post','2026-07-22 05:47:20','/feed#post45'),(128,10,'tahoor commented on your post','2026-07-22 05:47:25','/feed#post45'),(129,2,'tahoor shared a post with you','2026-07-22 05:47:31','/chat/1'),(130,2,'tahoor liked your post','2026-07-22 05:48:03','/feed#post57'),(131,2,'tahoor shared a post with you','2026-07-22 05:48:55','/chat/1'),(132,2,'tahoor liked your post','2026-07-22 06:00:25','/feed#post57'),(133,2,'tahoor commented on your post','2026-07-22 06:00:29','/feed#post57'),(134,5,'tahoor shared a post with you','2026-07-22 06:00:36','/chat/1'),(135,1,'Ali liked your post','2026-07-22 06:05:46','/feed#post55'),(136,1,'Ali commented on your post','2026-07-22 06:07:28','/feed#post55'),(137,1,'Ali shared a post with you','2026-07-22 06:07:40','/chat/2'),(138,1,'Ali commented on your post','2026-07-22 06:08:00','/feed#post55'),(139,1,'Ali liked your post','2026-07-22 06:08:06','/feed#post53'),(140,2,'tahoor liked your post','2026-07-22 11:37:55','/feed#post57'),(141,2,'tahoor liked your post','2026-07-22 12:15:44','/feed#post57'),(142,2,'tahoor liked your post','2026-07-22 12:17:34','/feed#post57');
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
INSERT INTO `posts` VALUES (1,'Hello EchoMateLite','2026-06-16 18:39:37',NULL,NULL),(45,'','2026-07-04 08:18:39',10,'0C61B5B6-1D61-4D63-AB16-B24C61B23611.jpg'),(50,'','2026-07-15 07:19:01',1,'IMG_20260604_210528458.jpeg'),(52,'','2026-07-15 08:21:32',1,'16590.jpg'),(53,'','2026-07-15 11:49:20',1,'18951.jpg'),(55,'\"They say the journey is more important than the destination, and after hundreds of kilometers behind the wheel, I finally understand why. There’s something meditative about the highway—the way the world blurs into a backdrop of trees, towns, and shifting landscapes while you’re focused on the road ahead. It’s just me, the engine, and the infinite horizon. Fueling up, shifting gears, and letting the miles wash everything else away.','2026-07-19 14:39:39',1,'IMG_2188.jpeg'),(57,'This is insane bruh🔥🔥🔥','2026-07-21 14:54:15',2,'15768.mp4');
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `saved_posts`
--

DROP TABLE IF EXISTS `saved_posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `saved_posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `post_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `saved_posts`
--

LOCK TABLES `saved_posts` WRITE;
/*!40000 ALTER TABLE `saved_posts` DISABLE KEYS */;
/*!40000 ALTER TABLE `saved_posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stories`
--

DROP TABLE IF EXISTS `stories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `media_url` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `stories_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stories`
--

LOCK TABLES `stories` WRITE;
/*!40000 ALTER TABLE `stories` DISABLE KEYS */;
INSERT INTO `stories` VALUES (26,1,'27594.mp4','2026-07-21 14:20:38');
/*!40000 ALTER TABLE `stories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `profile_pic` varchar(255) DEFAULT NULL,
  `bio` text,
  `last_seen` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'tahoor','syed@gmail.com','123456','2026-06-15 20:27:13','IMG_20260604_210528458.jpeg','something new coming up','2026-07-22 17:45:34'),(2,'Ali','ali@gmail.com','12345','2026-06-19 13:36:21','IMG_2431.jpeg','this is me','2026-07-22 11:38:22'),(4,'Ali01','ali01@gmail.com','123456','2026-06-19 13:37:59',NULL,NULL,NULL),(5,'user2','user2@gmail.com','123456','2026-06-19 13:55:03',NULL,NULL,NULL),(7,'echomate','echo@gmail.com','12345','2026-06-24 14:33:15','Photo_on_15-03-26_at_4.17_AM.jpg','this is my second project ','2026-06-24 22:17:02'),(8,'syedtahoor','syedtahoor023@gmail.com','12345','2026-06-24 17:07:18','Photo_on_15-03-26_at_4.17_AM.jpg',NULL,'2026-07-05 21:11:47'),(9,'ahsan','ahsan@gmail.com','12345','2026-06-24 17:18:57','IMG-20260623-WA0000.jpg',NULL,'2026-06-24 23:01:45'),(10,'shihaab','shihaab@gmail.com','pbkdf2:sha256:1000000$OlnWIiKvhi9I69yV$052695dc9a515cc1d84192975a036a12d1aca0b756ec357a82af07fd7bfc3c19','2026-07-04 06:05:00','0C61B5B6-1D61-4D63-AB16-B24C61B23611.jpg','sui','2026-07-22 02:35:54'),(11,'shihaab','shihaab1@gmail.com','pbkdf2:sha256:1000000$6cvGLPd3v9dde1j2$23ce148c2cebfc92ea4300599e17e829de32a4404c1689a8af35c90d2538e966','2026-07-04 06:06:06',NULL,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-22 17:56:48
