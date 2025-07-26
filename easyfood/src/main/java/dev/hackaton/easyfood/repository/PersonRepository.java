package dev.hackaton.easyfood.repository;

import java.util.Optional;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import dev.hackaton.easyfood.model.Person;

@Repository
public interface PersonRepository extends CrudRepository<Person, Integer> {
    Optional<Person> findPersonByTelephoneNumber(int phoneNumber);
}
