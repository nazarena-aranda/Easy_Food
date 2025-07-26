package dev.hackaton.easyfood.repository;

import java.util.List;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import dev.hackaton.easyfood.model.Dish;

@Repository
public interface DishRepository extends CrudRepository<Dish, Integer> {

    @Query("SELECT e FROM Dish e WHERE e.restaurant.id = ?1")
    List<Dish> getDishesFromRestaurant(int id);
    
}
