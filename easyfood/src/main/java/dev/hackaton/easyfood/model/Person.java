package dev.hackaton.easyfood.model;

import java.util.List;

import jakarta.persistence.CollectionTable;
import jakarta.persistence.Column;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.Data;

@Data
@Entity
@Table(name = "persons")
public class Person {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(name = "name", nullable = false, length = 45)
    private String name;

    @Column(name = "telephone_number", nullable = false, unique = true)
    private long telephoneNumber;

    @OneToMany(mappedBy = "person")
    private List<Review> reviews;

    @Column(name = "address", nullable = false, length = 200)
    private String address;

    @ElementCollection
    @CollectionTable(name = "person_allergies")
    private List<String> allergies;

    @ElementCollection
    @CollectionTable(name = "person_dislikes")
    private List<String> dislikes;

}
