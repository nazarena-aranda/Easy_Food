package dev.hackaton.easyfood.service;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.springframework.stereotype.Service;

import dev.hackaton.easyfood.dto.RestaurantDataDto;
import dev.hackaton.easyfood.model.Review;
import dev.hackaton.easyfood.repository.RestaurantRepository;
import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class RestaurantService {
    
    private RestaurantRepository repository;

    public RestaurantDataDto getRestaurantById(int id) {
        var restaurant = repository.findById(id).orElseThrow();
        return new RestaurantDataDto(
            restaurant.getId(),
            restaurant.getName(),
            restaurant.getX(),
            restaurant.getY(),
            this.calculateRestaurantRating(restaurant.getReviews())
        );
    }

    public Set<RestaurantDataDto> getAllRestaurantsData() {
        var restaurantList = new HashSet<RestaurantDataDto>();
        repository.findAll().forEach(data -> restaurantList.add(
            new RestaurantDataDto(
                data.getId(),
                data.getName(),
                data.getX(),
                data.getY(),
                this.calculateRestaurantRating(data.getReviews())
            )
        ));
        return restaurantList;
    }

    private short calculateRestaurantRating(List<Review> reviews) {
        int accumulator = 0;
        for (Review r : reviews) accumulator += r.getRating();
        return (short) (accumulator / reviews.size());
    }

}
