-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : ven. 24 juin 2022 à 09:02
-- Version du serveur :  10.4.17-MariaDB
-- Version de PHP : 7.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `triannot2022`
--

-- --------------------------------------------------------

--
-- Structure de la table `tr_analyse_ana`
--

CREATE TABLE `tr_analyse_ana` (
  `ana_id` int(11) NOT NULL,
  `ana_libelle` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `tr_analyse_ana`
--

INSERT INTO `tr_analyse_ana` (`ana_id`, `ana_libelle`) VALUES
(1, 'wheat_step220621_long'),
(2, 'wheat_step220621_short'),
(3, 'wheat_step220621_withFuncAnnot');

-- --------------------------------------------------------

--
-- Structure de la table `tr_delete_del`
--

CREATE TABLE `tr_delete_del` (
  `del_id` int(11) NOT NULL,
  `del_code` text NOT NULL,
  `del_date` varchar(255) NOT NULL,
  `del_login` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `tr_levels_lev`
--

CREATE TABLE `tr_levels_lev` (
  `lev_id` int(11) NOT NULL,
  `lev_libelle` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `tr_levels_lev`
--

INSERT INTO `tr_levels_lev` (`lev_id`, `lev_libelle`) VALUES
(-1, 'Admin'),
(0, 'TriAnnot user');

-- --------------------------------------------------------

--
-- Structure de la table `tr_statut_sta`
--

CREATE TABLE `tr_statut_sta` (
  `sta_id` int(11) NOT NULL,
  `sta_libelle` varchar(30) DEFAULT NULL,
  `sta_couleur` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `tr_statut_sta`
--

INSERT INTO `tr_statut_sta` (`sta_id`, `sta_libelle`, `sta_couleur`) VALUES
(0, 'pending', '#BFCEE0'),
(1, 'running', '#D2BF32'),
(2, 'finished', '#5BD671'),
(3, 'failed', '#EB7567');

-- --------------------------------------------------------

--
-- Structure de la table `tr_typemol_tmo`
--

CREATE TABLE `tr_typemol_tmo` (
  `tmo_id` int(10) NOT NULL,
  `tmo_libelle` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `tr_typemol_tmo`
--

INSERT INTO `tr_typemol_tmo` (`tmo_id`, `tmo_libelle`) VALUES
(1, 'nucleic'),
(2, 'proteic');

-- --------------------------------------------------------

--
-- Structure de la table `t_params_par`
--

CREATE TABLE `t_params_par` (
  `par_id` int(11) NOT NULL,
  `par_libelle` varchar(30) NOT NULL,
  `par_value` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `t_params_par`
--

INSERT INTO `t_params_par` (`par_id`, `par_libelle`, `par_value`) VALUES
(3, 'version', '2.0.0');

-- --------------------------------------------------------

--
-- Structure de la table `t_request_req`
--

CREATE TABLE `t_request_req` (
  `req_id` int(11) NOT NULL,
  `req_sequences` varchar(60) NOT NULL,
  `req_code` varchar(60) DEFAULT NULL,
  `req_statut` text DEFAULT NULL,
  `req_login` varchar(15) DEFAULT NULL,
  `req_date` varchar(255) NOT NULL,
  `req_tmo_id` int(11) NOT NULL,
  `req_min_size` int(11) NOT NULL,
  `req_max_size` int(11) NOT NULL,
  `req_splitseq` tinyint(1) NOT NULL,
  `req_overlap` int(11) NOT NULL DEFAULT 50000,
  `req_ana_id` int(11) NOT NULL,
  `req_progress` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_users_use`
--

CREATE TABLE `t_users_use` (
  `use_id` int(11) NOT NULL,
  `use_login` varchar(30) DEFAULT NULL,
  `use_mdp` varchar(355) DEFAULT NULL,
  `use_level` int(11) DEFAULT NULL,
  `use_mail` varchar(255) NOT NULL,
  `use_token` varchar(255) NOT NULL,
  `use_date_change` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `t_users_use`
--

INSERT INTO `t_users_use` (`use_id`, `use_login`, `use_mdp`, `use_level`, `use_mail`, `use_token`, `use_date_change`) VALUES
(6, 'micro', '15e19925dda65ae2ea3f57c4b7166a26', -1, '', '', '0000-00-00 00:00:00');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `tr_analyse_ana`
--
ALTER TABLE `tr_analyse_ana`
  ADD PRIMARY KEY (`ana_id`);

--
-- Index pour la table `tr_delete_del`
--
ALTER TABLE `tr_delete_del`
  ADD PRIMARY KEY (`del_id`);

--
-- Index pour la table `tr_levels_lev`
--
ALTER TABLE `tr_levels_lev`
  ADD PRIMARY KEY (`lev_id`);

--
-- Index pour la table `tr_statut_sta`
--
ALTER TABLE `tr_statut_sta`
  ADD PRIMARY KEY (`sta_id`);

--
-- Index pour la table `tr_typemol_tmo`
--
ALTER TABLE `tr_typemol_tmo`
  ADD PRIMARY KEY (`tmo_id`);

--
-- Index pour la table `t_params_par`
--
ALTER TABLE `t_params_par`
  ADD PRIMARY KEY (`par_id`);

--
-- Index pour la table `t_request_req`
--
ALTER TABLE `t_request_req`
  ADD PRIMARY KEY (`req_id`),
  ADD KEY `req_ana_id` (`req_ana_id`);

--
-- Index pour la table `t_users_use`
--
ALTER TABLE `t_users_use`
  ADD PRIMARY KEY (`use_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `tr_analyse_ana`
--
ALTER TABLE `tr_analyse_ana`
  MODIFY `ana_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `tr_typemol_tmo`
--
ALTER TABLE `tr_typemol_tmo`
  MODIFY `tmo_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `t_params_par`
--
ALTER TABLE `t_params_par`
  MODIFY `par_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `t_request_req`
--
ALTER TABLE `t_request_req`
  MODIFY `req_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `t_users_use`
--
ALTER TABLE `t_users_use`
  MODIFY `use_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `t_request_req`
--
ALTER TABLE `t_request_req`
  ADD CONSTRAINT `t_request_req_ibfk_1` FOREIGN KEY (`req_ana_id`) REFERENCES `tr_analyse_ana` (`ana_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
