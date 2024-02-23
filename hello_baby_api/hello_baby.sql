-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3307
-- Généré le : ven. 16 fév. 2024 à 10:57
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `hello_baby`
--

-- --------------------------------------------------------

--
-- Structure de la table `baby`
--

CREATE TABLE `baby` (
  `id_baby` int(8) NOT NULL,
  `firstname` varchar(56) NOT NULL,
  `lastname` varchar(56) DEFAULT NULL,
  `birthday` date NOT NULL,
  `size` int(8) DEFAULT NULL,
  `weight` int(8) DEFAULT NULL,
  `id_user` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `biberons`
--

CREATE TABLE `biberons` (
  `id_bib` int(8) NOT NULL,
  `quantity_drink` int(11) DEFAULT NULL,
  `nb_bib` int(11) DEFAULT NULL,
  `id_baby` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `forums`
--

CREATE TABLE `forums` (
  `id_forums` int(8) NOT NULL,
  `id_user` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `messages`
--

CREATE TABLE `messages` (
  `id_message` int(8) NOT NULL,
  `text_message` longtext NOT NULL,
  `id_forums` int(11) NOT NULL,
  `id_user` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `pregnancy`
--

CREATE TABLE `pregnancy` (
  `id_pregnancy` int(8) NOT NULL,
  `pregnancy_date` date NOT NULL,
  `amenorrhea_date` date NOT NULL,
  `id_user` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `id_user` int(8) NOT NULL,
  `firstname` varchar(256) NOT NULL,
  `lastname` varchar(256) DEFAULT NULL,
  `email` varchar(56) NOT NULL,
  `password` varchar(56) NOT NULL,
  `birthday` date DEFAULT NULL,
  `couple` tinyint(1) DEFAULT NULL,
  `weight` int(8) DEFAULT NULL,
  `picture_profil` binary(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`id_user`, `firstname`, `lastname`, `email`, `password`, `birthday`, `couple`, `weight`, `picture_profil`) VALUES
(1, 'Andrea', NULL, 'test@mail.fr', 'test', NULL, NULL, NULL, NULL);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `baby`
--
ALTER TABLE `baby`
  ADD PRIMARY KEY (`id_baby`),
  ADD UNIQUE KEY `id_user` (`id_user`);

--
-- Index pour la table `biberons`
--
ALTER TABLE `biberons`
  ADD PRIMARY KEY (`id_bib`),
  ADD UNIQUE KEY `id_baby` (`id_baby`);

--
-- Index pour la table `forums`
--
ALTER TABLE `forums`
  ADD PRIMARY KEY (`id_forums`),
  ADD UNIQUE KEY `id_user` (`id_user`);

--
-- Index pour la table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id_message`),
  ADD UNIQUE KEY `id_user` (`id_user`),
  ADD UNIQUE KEY `id_forums` (`id_forums`) USING BTREE;

--
-- Index pour la table `pregnancy`
--
ALTER TABLE `pregnancy`
  ADD PRIMARY KEY (`id_pregnancy`),
  ADD UNIQUE KEY `id_user` (`id_user`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `baby`
--
ALTER TABLE `baby`
  MODIFY `id_baby` int(8) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `biberons`
--
ALTER TABLE `biberons`
  MODIFY `id_bib` int(8) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `forums`
--
ALTER TABLE `forums`
  MODIFY `id_forums` int(8) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `messages`
--
ALTER TABLE `messages`
  MODIFY `id_message` int(8) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `pregnancy`
--
ALTER TABLE `pregnancy`
  MODIFY `id_pregnancy` int(8) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `baby`
--
ALTER TABLE `baby`
  ADD CONSTRAINT `baby_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `biberons`
--
ALTER TABLE `biberons`
  ADD CONSTRAINT `biberons_ibfk_1` FOREIGN KEY (`id_baby`) REFERENCES `baby` (`id_baby`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `forums`
--
ALTER TABLE `forums`
  ADD CONSTRAINT `forums_ibfk_1` FOREIGN KEY (`id_forums`) REFERENCES `messages` (`id_forums`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `forums_ibfk_2` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `pregnancy`
--
ALTER TABLE `pregnancy`
  ADD CONSTRAINT `pregnancy_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
