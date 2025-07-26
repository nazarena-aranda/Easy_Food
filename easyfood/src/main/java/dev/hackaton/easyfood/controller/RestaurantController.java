package dev.hackaton.easyfood.controller;

import java.util.Set;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import dev.hackaton.easyfood.dto.RestaurantDataDto;
import dev.hackaton.easyfood.service.RestaurantService;
import lombok.AllArgsConstructor;

@RestController
@RequestMapping("/restaurant")
@AllArgsConstructor
public class RestaurantController {
    
    private RestaurantService restaurantService;

    @GetMapping("/{id}")
    @ResponseStatus(HttpStatus.OK)
    public RestaurantDataDto getRestaurantById(@PathVariable(required = true) int id) {
        return restaurantService.getRestaurantById(id);
    }

    @GetMapping
    @ResponseStatus(HttpStatus.OK)
    public Set<RestaurantDataDto> getAllRestaurantsData() {
        return restaurantService.getAllRestaurantsData();
    }

    

}
