package dev.hackaton.easyfood.model;

import java.math.BigDecimal;
import java.util.Set;

import jakarta.persistence.CollectionTable;
import jakarta.persistence.Column;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Data;

@Data
@Entity
@Table(name = "dishes")
public class Dish {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(name = "name", nullable = false, length = 45)
    private String name;

    @Column(name = "price", nullable = false)
    private BigDecimal price;
    
    @ManyToOne
    @JoinColumn(name = "FK_INVOICE")
    private Restaurant restaurant;

    @ElementCollection
    @CollectionTable(name = "dish_ingredients")
    private Set<String> ingredients;
    
}
