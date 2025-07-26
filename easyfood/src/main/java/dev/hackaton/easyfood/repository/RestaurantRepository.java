package dev.hackaton.easyfood.repository;

import java.util.List;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import dev.hackaton.easyfood.model.Restaurant;

@Repository
public interface RestaurantRepository extends CrudRepository<Restaurant, Integer> {

    @Query(value = """
            SELECT * FROM restaurants
            WHERE ST_Distance(
                ST_GeomFromText(CONCAT('POINT(', coordinate_x, ' ', coordinate_y, ')')),
                ST_GeomFromText('POINT(:x :y)')
            ) <= :radius
            """, nativeQuery = true)
    List<Restaurant> findNearbyRestaurantsOnRadius(double x, double y, int radius);
}