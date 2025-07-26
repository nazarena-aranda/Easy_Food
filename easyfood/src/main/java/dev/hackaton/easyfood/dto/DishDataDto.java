package dev.hackaton.easyfood.dto;

import java.math.BigDecimal;
import java.util.List;

public record DishDataDto(long id, String name, BigDecimal price, List<String> ingredients) {}
