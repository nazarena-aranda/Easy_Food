package dev.hackaton.easyfood.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import dev.hackaton.easyfood.dto.DishDataDto;
import dev.hackaton.easyfood.model.Dish;
import dev.hackaton.easyfood.repository.DishRepository;
import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class DishService {

    private DishRepository dishRepository;

    public List<DishDataDto> getDishesFromRestaurant(int restaurantId) {
        List<Dish> dishes = dishRepository.getDishesFromRestaurant(restaurantId);
        List<DishDataDto> data = new ArrayList<>(dishes.size());

        dishes.forEach(d -> data.add(new DishDataDto(
                d.getId(),
                d.getName(),
                d.getPrice(),
                d.getIngredients().stream().toList())));

        return data;
    }
}
