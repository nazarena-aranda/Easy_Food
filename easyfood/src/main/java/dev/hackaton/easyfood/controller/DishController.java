package dev.hackaton.easyfood.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import dev.hackaton.easyfood.dto.DishDataDto;
import dev.hackaton.easyfood.service.DishService;
import lombok.AllArgsConstructor;

@RestController
@RequestMapping("/dish")
@AllArgsConstructor
public class DishController {

    private DishService dishService;

    @GetMapping("/{id}")
    public List<DishDataDto> getDishesFromRestaurant(@PathVariable(value = "id") int restaurantId) {
        return dishService.getDishesFromRestaurant(restaurantId);
    }


}
