-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema cinepedia
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema cinepedia
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cinepedia` DEFAULT CHARACTER SET utf8 ;
USE `cinepedia` ;

-- -----------------------------------------------------
-- Table `cinepedia`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cinepedia`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NULL,
  `apellido` VARCHAR(100) NULL,
  `email` VARCHAR(255) NULL,
  `contrasena` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cinepedia`.`peliculas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cinepedia`.`peliculas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_pelicula` VARCHAR(255) NULL,
  `director` VARCHAR(45) NULL,
  `fecha_estreno` DATE NULL,
  `sinopsis` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_peliculas_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_peliculas_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `cinepedia`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cinepedia`.`comentarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cinepedia`.`comentarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `comentario` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_id` INT NOT NULL,
  `pelicula_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comentarios_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  INDEX `fk_comentarios_peliculas1_idx` (`pelicula_id` ASC) VISIBLE,
  CONSTRAINT `fk_comentarios_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `cinepedia`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comentarios_peliculas1`
    FOREIGN KEY (`pelicula_id`)
    REFERENCES `cinepedia`.`peliculas` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
