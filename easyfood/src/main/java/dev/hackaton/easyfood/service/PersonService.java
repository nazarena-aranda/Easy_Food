package dev.hackaton.easyfood.service;

import org.springframework.stereotype.Service;

import dev.hackaton.easyfood.dto.CreatePersonDto;
import dev.hackaton.easyfood.model.Person;
import dev.hackaton.easyfood.repository.PersonRepository;
import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class PersonService {

    private PersonRepository personRepository;

    public void createPerson(CreatePersonDto dto) {

        Person person = new Person();
        person.setName(dto.name());
        person.setTelephoneNumber(dto.telephoneNumber());
        person.setAllergies(dto.allergies());
        person.setDislikes(dto.dislikes());

        personRepository.save(person);

    }
    
}
