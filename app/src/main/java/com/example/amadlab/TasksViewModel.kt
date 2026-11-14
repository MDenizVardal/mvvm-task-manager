package com.example.amadlab

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn

// Task 3.2: the filter from task 2.2.4, now owned by the view model
enum class TaskFilter(val label: String) { ALL("All"), ACTIVE("Active"), DONE("Done") }

data class TasksUiState(
    val tasks: List<Task> = emptyList(),      // already filtered - the screen only shows it
    val newTitle: String = "",
    val filter: TaskFilter = TaskFilter.ALL,
    val totalCount: Int = 0,                  // counted on the whole list, not the filtered one
    val doneCount: Int = 0
) {
    val canAdd: Boolean get() = newTitle.isNotBlank()
}

class TasksViewModel(
    private val repository: TaskRepository = TaskRepository
) : ViewModel() {

    private val newTitle = MutableStateFlow("")
    private val filter = MutableStateFlow(TaskFilter.ALL)

    init {
        Log.d("ViewModel", "TasksViewModel created")
    }

    // Task 3.2: combine takes three flows; a new UI state is emitted when any of them changes
    val uiState: StateFlow<TasksUiState> =
        combine(repository.tasks, newTitle, filter) { tasks, title, selected ->
            TasksUiState(
                tasks = when (selected) {
                    TaskFilter.ALL -> tasks
                    TaskFilter.ACTIVE -> tasks.filter { !it.done }
                    TaskFilter.DONE -> tasks.filter { it.done }
                },
                newTitle = title,
                filter = selected,
                totalCount = tasks.size,
                doneCount = tasks.count { it.done }
            )
        }.stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = TasksUiState()
        )

    fun onTitleChange(title: String) {
        newTitle.value = title
    }

    fun onFilterChange(selected: TaskFilter) {
        filter.value = selected
    }

    fun addTask() {
        if (newTitle.value.isBlank()) return
        repository.add(newTitle.value)
        newTitle.value = ""
    }

    fun toggle(id: Long) = repository.toggle(id)

    override fun onCleared() {
        Log.d("ViewModel", "TasksViewModel cleared")
    }
}
