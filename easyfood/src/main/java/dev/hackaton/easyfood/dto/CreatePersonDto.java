package dev.hackaton.easyfood.dto;

import java.util.List;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;

public record CreatePersonDto(

    @NotBlank(message = "Name must not be null or blank")
    @Size(min = 1, max = 45, message = "Name must be between 1 and 45 characters")
    String name,

    @NotNull
    @Positive(message = "Telephone number must be positive")
    long telephoneNumber,

    @NotBlank
    @Size(min = 1, max = 200)
    String address,

    @NotNull
    List<String> allergies,

    @NotNull
    List<String> dislikes
    
    )
    
{}
