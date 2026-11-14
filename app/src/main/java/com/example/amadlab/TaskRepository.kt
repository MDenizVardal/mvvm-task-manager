package com.example.amadlab

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

// Single source of truth for the tasks (listing 1). Only this object changes the list.
object TaskRepository {
    private val _tasks = MutableStateFlow(
        listOf(
            Task(1, "Install Android Studio", done = true),
            Task(2, "Learn Compose"),
            Task(3, "Read about MVVM")
        )
    )
    val tasks: StateFlow<List<Task>> = _tasks.asStateFlow()
    private var nextId = 4L

    fun add(title: String) {
        // the id is taken before update { }, because update may run its lambda more than once
        val id = nextId++
        _tasks.update { it + Task(id, title.trim()) }
    }

    fun toggle(id: Long) {
        _tasks.update { list -> list.map { if (it.id == id) it.copy(done = !it.done) else it } }
    }

    fun delete(id: Long) {
        _tasks.update { list -> list.filter { it.id != id } }
    }

    // Task 3.3: change the title of one task
    fun rename(id: Long, title: String) {
        _tasks.update { list -> list.map { if (it.id == id) it.copy(title = title.trim()) else it } }
    }

    fun find(id: Long): Task? = _tasks.value.find { it.id == id }
}
