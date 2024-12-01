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
-- Table structure for table `grades`
--

DROP TABLE IF EXISTS `grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `assignment_id` int NOT NULL,
  `grade` decimal(5,2) NOT NULL,
  `feedback` text,
  `graded_by` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `assignment_id` (`assignment_id`),
  KEY `graded_by` (`graded_by`),
  CONSTRAINT `grades_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `grades_ibfk_2` FOREIGN KEY (`assignment_id`) REFERENCES `assignments` (`id`) ON DELETE CASCADE,
  CONSTRAINT `grades_ibfk_3` FOREIGN KEY (`graded_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades`
--

LOCK TABLES `grades` WRITE;
/*!40000 ALTER TABLE `grades` DISABLE KEYS */;
INSERT INTO `grades` VALUES (1,4,1,10.00,'Keep trying! Check your answers.',NULL,'2024-11-26 15:56:40','2024-11-26 15:56:40'),(2,4,1,10.00,'Keep trying! Check your answers.',NULL,'2024-11-26 15:56:55','2024-11-26 15:56:55'),(3,4,1,10.00,'Keep trying! Check your answers.',NULL,'2024-11-26 16:24:05','2024-11-26 16:24:05'),(4,4,1,0.00,'Keep trying! Check your answers.',NULL,'2024-11-26 16:32:16','2024-11-26 16:32:16'),(5,4,1,20.00,'Well done!',NULL,'2024-11-26 16:40:26','2024-11-26 16:40:26'),(6,4,1,0.00,'Keep trying! Check your answers.',NULL,'2024-11-26 16:51:18','2024-11-26 16:51:18'),(7,4,1,0.00,'Keep trying! Check your answers.',NULL,'2024-11-26 16:53:27','2024-11-26 16:53:27'),(8,4,1,20.00,'Well done!',NULL,'2024-11-26 16:55:33','2024-11-26 16:55:33'),(9,4,1,20.00,'Well done!',NULL,'2024-11-26 16:57:18','2024-11-26 16:57:18'),(10,4,2,20.00,'Well done!',NULL,'2024-11-26 17:10:34','2024-11-26 17:10:34'),(11,4,2,20.00,'Well done!',NULL,'2024-11-26 17:14:55','2024-11-26 17:14:55'),(12,4,1,20.00,'Well done!',NULL,'2024-11-27 16:02:02','2024-11-27 16:02:02'),(13,4,1,10.00,'Keep trying! Check your answers.',NULL,'2024-11-28 15:24:16','2024-11-28 15:24:16');
/*!40000 ALTER TABLE `grades` ENABLE KEYS */;
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
