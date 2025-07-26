package dev.hackaton.easyfood.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import dev.hackaton.easyfood.model.Restaurant;
import dev.hackaton.easyfood.model.Review;

public interface ReviewRepository extends JpaRepository<Review, Long> {
    
    @Query("SELECT AVG(r.rating) FROM Review r WHERE r.restaurant = :restaurant")
    Double findAverageRatingByRestaurant(Restaurant restaurant);

}