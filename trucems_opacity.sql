-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 17, 2022 at 07:23 AM
-- Server version: 5.7.33
-- PHP Version: 7.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `trucems_opacity`
--

-- --------------------------------------------------------

--
-- Table structure for table `configurations`
--

CREATE TABLE `configurations` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `is_calibration` smallint(6) DEFAULT '0' COMMENT '0 = Nothing, 1 = Auto, 2 = Manual',
  `date_and_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `configurations`
--

INSERT INTO `configurations` (`id`, `is_calibration`, `date_and_time`, `created_at`, `updated_at`) VALUES
(1, 0, '2022-09-14 02:52:56', '2022-09-14 02:52:56', '2022-09-14 02:52:56');

-- --------------------------------------------------------

--
-- Table structure for table `migrations`
--

CREATE TABLE `migrations` (
  `id` int(10) UNSIGNED NOT NULL,
  `migration` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `batch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(1, '2022_05_24_030051_create_configurations_table', 1),
(2, '2022_05_24_030858_create_units_table', 1),
(3, '2022_05_24_030903_create_sensors_table', 1),
(4, '2022_05_24_031237_create_sensor_values_table', 1),
(5, '2022_05_30_172616_create_runtime_table', 1);

-- --------------------------------------------------------

--
-- Table structure for table `runtime`
--

CREATE TABLE `runtime` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `days` double DEFAULT '0',
  `hours` double DEFAULT '0',
  `minutes` double DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `runtime`
--

INSERT INTO `runtime` (`id`, `days`, `hours`, `minutes`, `created_at`, `updated_at`) VALUES
(1, 0, 0, 1, '2022-09-14 02:52:56', '2022-09-14 02:52:56');

-- --------------------------------------------------------

--
-- Table structure for table `sensors`
--

CREATE TABLE `sensors` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `unit_id` bigint(20) UNSIGNED DEFAULT NULL,
  `code` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Render HTML Value',
  `read_formula` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `write_address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `analog_formula` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `sensors`
--

INSERT INTO `sensors` (`id`, `unit_id`, `code`, `name`, `read_formula`, `write_address`, `analog_formula`, `created_at`, `updated_at`) VALUES
(1, 1, 'opacity', 'Opacity', 'round((0.00625 * value) - 25, 1)', '0', NULL, NULL, '2022-09-14 14:12:57');

-- --------------------------------------------------------

--
-- Table structure for table `sensor_values`
--

CREATE TABLE `sensor_values` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `sensor_id` bigint(20) UNSIGNED DEFAULT NULL,
  `value` double DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `sensor_values`
--

INSERT INTO `sensor_values` (`id`, `sensor_id`, `value`, `created_at`, `updated_at`) VALUES
(1, 1, -1, NULL, '2022-09-14 03:39:49');

-- --------------------------------------------------------

--
-- Table structure for table `units`
--

CREATE TABLE `units` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `units`
--

INSERT INTO `units` (`id`, `name`, `created_at`, `updated_at`) VALUES
(1, '%', NULL, NULL),
(2, 'ppm', NULL, NULL),
(3, 'μg/m3', NULL, NULL),
(4, 'mg/m3', NULL, NULL),
(5, 'l/min', NULL, NULL),
(6, 'm3/min', NULL, NULL),
(7, 'minutes', NULL, NULL),
(8, 'ton', NULL, NULL),
(9, 'm/sec', NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `configurations`
--
ALTER TABLE `configurations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `runtime`
--
ALTER TABLE `runtime`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sensors`
--
ALTER TABLE `sensors`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sensors_unit_id_foreign` (`unit_id`);

--
-- Indexes for table `sensor_values`
--
ALTER TABLE `sensor_values`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sensor_values_sensor_id_foreign` (`sensor_id`);

--
-- Indexes for table `units`
--
ALTER TABLE `units`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `configurations`
--
ALTER TABLE `configurations`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `runtime`
--
ALTER TABLE `runtime`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `sensors`
--
ALTER TABLE `sensors`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `sensor_values`
--
ALTER TABLE `sensor_values`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `units`
--
ALTER TABLE `units`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sensors`
--
ALTER TABLE `sensors`
  ADD CONSTRAINT `sensors_unit_id_foreign` FOREIGN KEY (`unit_id`) REFERENCES `units` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `sensor_values`
--
ALTER TABLE `sensor_values`
  ADD CONSTRAINT `sensor_values_sensor_id_foreign` FOREIGN KEY (`sensor_id`) REFERENCES `sensors` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
