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
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `assignment_id` int NOT NULL,
  `question_type` varchar(50) NOT NULL,
  `question_text` text NOT NULL,
  `correct_answer` text,
  `option_a` varchar(255) DEFAULT NULL,
  `option_b` varchar(255) DEFAULT NULL,
  `option_c` varchar(255) DEFAULT NULL,
  `option_d` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `assignment_id` (`assignment_id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`assignment_id`) REFERENCES `assignments` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (1,1,'FIB','4+2','6',NULL,NULL,NULL,NULL),(2,1,'MCQ','4+3','D','1','2','3','7'),(3,2,'FIB','The way parameters in the mind help people to be creative\r\n','E','','','',''),(4,2,'FIB','The need to learn rules in order to break them\r\n','C','','','',''),(5,2,'FIB','How habits restrict us and limit creativity\r\n','A','','','',''),(6,2,'FIB','How to train the mind to be creative','D','','','',''),(7,2,'FIB','How the mind is trapped by the desire for order\r\n','B','','','',''),(8,2,'MCQ','According to the writer, creative people....\r\n','C','are usually born with their talents','are born with their talents','are not born with their talents ','are geniuses'),(9,2,'MCQ','According to the writer, creative people....','C','a gift from God or nature','an automatic response','difficult for many people to achieve','a well-trodden path'),(10,2,'MCQ','According to the writer,...\r\n','D','the human race\'s fight to live is becoming a tyranny','the human brain is blocked with cholesterol','the human race is now circumscribed by talents','the human race\'s fight to survive stifles creative ability'),(11,2,'MCQ','Advancing technology...','A','holds creativity in check','improves creativity','enhances creativity','is a tyranny'),(12,2,'MCQ','According to the author, creativity...\r\n','D',' is common','is increasingly common','is becoming rarer and rarer',' is a rare commodity'),(13,2,'FIB','Rules and regulations are examples of parameters.\r\n','Y','','','',''),(14,2,'FIB','The truly creative mind is associated with the need for free speech and a totally free society.\r\n','NG','','','',''),(15,2,'FIB','One problem with creativity is that people think it is impossible.\r\n','Y','','','',''),(16,2,'FIB','The act of creation is linked to madness.\r\n','Y','','','',''),(17,2,'FIB','Parameters help the mind by holding ideas and helping them to develop.\r\n','Y','','','','');
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
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
