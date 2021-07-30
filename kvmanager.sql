-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: 10.122.110.80    Database: kvmanager
-- ------------------------------------------------------
-- Server version	5.7.34

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
-- Table structure for table `computes`
--

DROP TABLE IF EXISTS `computes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `computes` (
  `token` char(32) COLLATE utf8mb4_bin NOT NULL COMMENT '使用MD5对hostip、user、password字段加密，作为主键，及校验字段',
  `hostip` varchar(16) COLLATE utf8mb4_bin NOT NULL COMMENT '宿主机ip地址，目前是全局唯一',
  `user` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '连接用户，可以为空，除tls连接外，一般都不设置用户',
  `password` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '登陆密码，可以为空，与user共同使用',
  `type` smallint(6) NOT NULL COMMENT '连接类型，1:tcp,2:ssh,3:tls,4:socket',
  `last_login` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近一次登录时间',
  `delete_sig` smallint(6) NOT NULL DEFAULT '0' COMMENT '删除标志，0为未删除，1为删除',
  PRIMARY KEY (`token`),
  UNIQUE KEY `hostname_UNIQUE` (`hostip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='宿主机连接表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `history_info`
--

DROP TABLE IF EXISTS `history_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `history_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增长ID',
  `custom_ip` varchar(16) COLLATE utf8mb4_bin NOT NULL COMMENT '操作发起的浏览器的IP地址',
  `host_ip` varchar(16) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '宿主机ip',
  `openstacks_name` varchar(300) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '本次操作上传的openstack平台名字',
  `openstacks_ip` varchar(300) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '本次操作上传的openstack平台ip',
  `image_name` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '上传镜像名字',
  `checksum` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '镜像md5值',
  `action` varchar(400) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '该操作完成情况',
  `status` varchar(10) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '整个请求完成状态',
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '上传操作开始时间',
  `end_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传操作结束时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='记录系统主要日志信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `openstack`
--

DROP TABLE IF EXISTS `openstack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `openstack` (
  `id_md5` varchar(32) COLLATE utf8mb4_bin NOT NULL COMMENT '根据其他字段(除token外)通过MD5加密的字符串，用作唯一id和校验方式',
  `platename` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '平台名称，该字段不属于连接字符串字段',
  `auth_ip` varchar(16) COLLATE utf8mb4_bin NOT NULL COMMENT '授权ip，即openstack服务器地址',
  `user_name` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'keystone连接符字段之一，username和userid选一个使用',
  `user_id` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'keystone连接符字段之一，username和userid选一个使用',
  `password` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'keystone连接符字段之一，配合username或userid使用',
  `domain_name` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'keystone连接符字段之一，与domain_id二选一',
  `domain_id` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'keystone连接符字段之一，与domain_name二选一',
  `token` varchar(200) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '在keystone认证得到的token令牌',
  `delete_sig` smallint(6) DEFAULT '0' COMMENT '删除标志，0代表未删除，1代表删除',
  PRIMARY KEY (`id_md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='openstack连接信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `upload_image`
--

DROP TABLE IF EXISTS `upload_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `upload_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `running_md5` varchar(32) COLLATE utf8mb4_bin NOT NULL COMMENT '根据image-running目录中的该文件生成的md5',
  `upload_md5` varchar(32) COLLATE utf8mb4_bin NOT NULL COMMENT '根据image-upload文件数据生成的md5值',
  `image_path` varchar(200) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文件地址',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '文件MD5生成时间',
  `delete_sig` smallint(6) DEFAULT '0' COMMENT '操作标志',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='image-upload目录中，raw格式镜像文件md5值信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` char(32) COLLATE utf8mb4_bin NOT NULL,
  `username` varchar(64) COLLATE utf8mb4_bin NOT NULL,
  `name` varchar(60) COLLATE utf8mb4_bin NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_bin NOT NULL,
  `phone` varchar(11) COLLATE utf8mb4_bin NOT NULL,
  `gender` char(1) COLLATE utf8mb4_bin NOT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-30 10:30:54
