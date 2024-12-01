CREATE DATABASE  IF NOT EXISTS `english_learning` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `english_learning`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: english_learning
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `lessons`
--

DROP TABLE IF EXISTS `lessons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lessons` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `content` longtext,
  `course_id` int DEFAULT NULL,
  `video_url` text,
  `file_path` text,
  `video_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `lessons_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lessons`
--

LOCK TABLES `lessons` WRITE;
/*!40000 ALTER TABLE `lessons` DISABLE KEYS */;
INSERT INTO `lessons` VALUES (1,'Intro-starter','learn simple alphabet',1,'https://www.youtube.com/watch?v=ezmsrB59mj8&pp=ygUNYWxwaGFiZXQgc29uZw%3D%3D','uploads/A-Z-Alphabet-Book-and-1-10.pdf','uploads/alphabet-song-test-sound.mp4'),(2,'lesson 1 : alphabet','learn how to speak alphabet better',1,'https://www.youtube.com/watch?v=ccEpTTZW34g&pp=ygUNYWxwaGFiZXQgc29uZw%3D%3D',NULL,'uploads/colors.mp4'),(6,'lesson 2 :colors ','learn colors',1,'','static/uploads/colours.pdf','static/uploads/colors.mp4'),(7,'lesson 3 : animal ','learning how to spell animals',1,'',NULL,'uploads/colors.mp4'),(8,'lesson 4 : cars','learn kind of cars',1,'https://www.youtube.com/watch?v=sJSGEQgAYWg&pp=ygUOY2FycyBmb3Iga8SxZHM%3D',NULL,NULL),(16,'.lesson5 : toys','learning about toys ',1,'https://www.youtube.com/watch?v=TJEjPTkQaTI&pp=ygUVdG95cyBmb3Iga2lkIGxlYXJuaW5n','static/uploads/Toys-vocabulary-worksheets-PDF.pdf','static/uploads/alphabet-song-test-sound.mp4'),(17,'.lesson5 : toys','learning about toys ',1,'https://www.youtube.com/watch?v=TJEjPTkQaTI&pp=ygUVdG95cyBmb3Iga2lkIGxlYXJuaW5n','static/uploads/Toys-vocabulary-worksheets-PDF.pdf','static/uploads/alphabet-song-test-sound.mp4'),(18,'.lesson5 : toys','learning about toys ',1,'https://www.youtube.com/watch?v=TJEjPTkQaTI&pp=ygUVdG95cyBmb3Iga2lkIGxlYXJuaW5n','static/uploads/Toys-vocabulary-worksheets-PDF.pdf','static/uploads/alphabet-song-test-sound.mp4'),(19,'.lesson5 : toys','learning about toys ',1,'https://www.youtube.com/watch?v=TJEjPTkQaTI&pp=ygUVdG95cyBmb3Iga2lkIGxlYXJuaW5n','static/uploads/Toys-vocabulary-worksheets-PDF.pdf','static/uploads/alphabet-song-test-sound.mp4'),(20,'.lesson5 : toys','learning about toys ',1,'https://www.youtube.com/watch?v=TJEjPTkQaTI&pp=ygUVdG95cyBmb3Iga2lkIGxlYXJuaW5n','static/uploads/Toys-vocabulary-worksheets-PDF.pdf','static/uploads/alphabet-song-test-sound.mp4');
/*!40000 ALTER TABLE `lessons` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-01 16:07:38
