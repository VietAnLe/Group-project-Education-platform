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
-- Table structure for table `student_answers`
--

DROP TABLE IF EXISTS `student_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_answers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `assignment_id` int NOT NULL,
  `question_id` int NOT NULL,
  `answer` text,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `assignment_id` (`assignment_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `student_answers_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`),
  CONSTRAINT `student_answers_ibfk_2` FOREIGN KEY (`assignment_id`) REFERENCES `assignments` (`id`),
  CONSTRAINT `student_answers_ibfk_3` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_answers`
--

LOCK TABLES `student_answers` WRITE;
/*!40000 ALTER TABLE `student_answers` DISABLE KEYS */;
INSERT INTO `student_answers` VALUES (2,4,1,1,''),(3,4,1,2,'7'),(4,4,1,1,''),(5,4,1,2,'7'),(6,4,1,1,''),(7,4,1,2,'d'),(8,4,1,1,'5'),(9,4,1,2,'d'),(10,4,1,1,'5'),(11,4,1,2,'D'),(12,4,1,1,'5'),(13,4,1,2,'d'),(14,4,1,1,'5'),(15,4,1,2,'D'),(16,4,1,1,'5'),(17,4,1,2,'D'),(18,4,1,1,'5'),(19,4,1,2,'D'),(20,4,2,3,'E'),(21,4,2,4,'C'),(22,4,2,5,'A'),(23,4,2,6,'D'),(24,4,2,7,'B'),(25,4,2,8,'C'),(26,4,2,9,'C'),(27,4,2,10,'D'),(28,4,2,11,'A'),(29,4,2,12,'D'),(30,4,2,13,'Y'),(31,4,2,14,'Ng'),(32,4,2,15,'y'),(33,4,2,16,'Y'),(34,4,2,17,'Y'),(35,4,2,3,'e'),(36,4,2,4,'c'),(37,4,2,5,'A'),(38,4,2,6,'D'),(39,4,2,7,'B'),(40,4,2,8,'C'),(41,4,2,9,'C'),(42,4,2,10,'D'),(43,4,2,11,'A'),(44,4,2,12,'D'),(45,4,2,13,'Y'),(46,4,2,14,'Ng'),(47,4,2,15,'y'),(48,4,2,16,'Y'),(49,4,2,17,'Y'),(50,4,1,1,'5'),(51,4,1,2,'D'),(52,4,1,1,'5'),(53,4,1,2,'D');
/*!40000 ALTER TABLE `student_answers` ENABLE KEYS */;
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
