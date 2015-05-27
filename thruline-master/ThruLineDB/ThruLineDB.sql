-- phpMyAdmin SQL Dump
-- version 4.2.7.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 12, 2015 at 09:39 PM
-- Server version: 5.6.20
-- PHP Version: 5.5.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ThruLineDB`
--

-- --------------------------------------------------------

--
-- Table structure for table `ACTORS`
--

CREATE TABLE IF NOT EXISTS `ACTORS` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(255) DEFAULT NULL,
  `photo_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ACTORS`
--

INSERT INTO `ACTORS` (`id`, `name`, `photo_url`) VALUES
(43, 'test', 'test');

-- --------------------------------------------------------

--
-- Table structure for table `CHARACTERS`
--

CREATE TABLE IF NOT EXISTS `CHARACTERS` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(255) DEFAULT NULL,
  `show_id` int(11) DEFAULT NULL,
  `actor_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `CHARACTERS`
--

INSERT INTO `CHARACTERS` (`id`, `name`, `show_id`, `actor_id`) VALUES
(99, 'test', 67, 89);

-- --------------------------------------------------------

--
-- Table structure for table `DIALOGUES`
--

CREATE TABLE IF NOT EXISTS `DIALOGUES` (
  `id` int(11) NOT NULL DEFAULT '0',
  `character_id` int(11) DEFAULT NULL,
  `raw_text` varchar(255) DEFAULT NULL,
  `keyword` varchar(255) DEFAULT NULL,
  `start_time` int(11) DEFAULT NULL,
  `end_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `DIALOGUES`
--

INSERT INTO `DIALOGUES` (`id`, `character_id`, `raw_text`, `keyword`, `start_time`, `end_time`) VALUES
(99, 2, 'test', 'test', 100, 999);

-- --------------------------------------------------------

--
-- Table structure for table `REQUESTS`
--

CREATE TABLE IF NOT EXISTS `REQUESTS` (
  `id` int(11) NOT NULL DEFAULT '0',
  `request` longtext
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `REQUESTS`
--

INSERT INTO `REQUESTS` (`id`, `request`) VALUES
(123, 'wqndlnlqwdl  nwldnlenwdnldw  n   ldnlendl    nlnewldnl   nqwlnw  dlnldnw ndn920102fekdnckn 88 jj');

-- --------------------------------------------------------

--
-- Table structure for table `SHOWS`
--

CREATE TABLE IF NOT EXISTS `SHOWS` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(255) DEFAULT NULL,
  `video_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `SHOWS`
--

INSERT INTO `SHOWS` (`id`, `name`, `video_url`) VALUES
(24, 'frnds', '/video/fr1/');

-- --------------------------------------------------------

--
-- Table structure for table `VIDEOS`
--

CREATE TABLE IF NOT EXISTS `VIDEOS` (
  `id` int(11) NOT NULL DEFAULT '0',
  `season_id` int(11) DEFAULT NULL,
  `episode_no` int(11) DEFAULT NULL,
  `episode_url` varchar(255) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `VIDEOS`
--

INSERT INTO `VIDEOS` (`id`, `season_id`, `episode_no`, `episode_url`, `duration`) VALUES
(4, 5, 6, '/foo/video/floder', 203);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ACTORS`
--
ALTER TABLE `ACTORS`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `CHARACTERS`
--
ALTER TABLE `CHARACTERS`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `DIALOGUES`
--
ALTER TABLE `DIALOGUES`
 ADD PRIMARY KEY (`id`), ADD FULLTEXT KEY `raw_text` (`raw_text`,`keyword`);

--
-- Indexes for table `REQUESTS`
--
ALTER TABLE `REQUESTS`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `SHOWS`
--
ALTER TABLE `SHOWS`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `VIDEOS`
--
ALTER TABLE `VIDEOS`
 ADD PRIMARY KEY (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
