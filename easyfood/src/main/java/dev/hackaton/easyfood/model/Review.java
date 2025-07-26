package dev.hackaton.easyfood.model;

import jakarta.persistence.Column;
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
@Table(name = "reviews")
public class Review {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @ManyToOne
    @JoinColumn(name = "FK_PERSON", nullable = false)
    private Person person;

    @ManyToOne
    @JoinColumn(name = "FK_RESTAURANT", nullable = false)
    private Restaurant restaurant;

    @Column(name = "description", nullable = false, length = 200)
    private String description;

    private short rating;

}
