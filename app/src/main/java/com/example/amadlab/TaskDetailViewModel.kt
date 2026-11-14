package com.example.amadlab

import android.util.Log
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.navigation.toRoute
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn

data class TaskDetailUiState(
    val task: Task? = null,
    val editedTitle: String = ""              // task 3.3: text of the title field
) {
    val canSave: Boolean
        get() = task != null && editedTitle.isNotBlank() && editedTitle.trim() != task.title
}

class TaskDetailViewModel(savedStateHandle: SavedStateHandle) : ViewModel() {

    // the navigation argument of the route TaskDetail(taskId)
    private val taskId: Long = savedStateHandle.toRoute<TaskDetail>().taskId

    private val editedTitle = MutableStateFlow(TaskRepository.find(taskId)?.title ?: "")

    init {
        Log.d("ViewModel", "TaskDetailViewModel created for task $taskId")
    }

    val uiState: StateFlow<TaskDetailUiState> =
        combine(
            TaskRepository.tasks.map { tasks -> tasks.find { it.id == taskId } },
            editedTitle
        ) { task, title ->
            TaskDetailUiState(task = task, editedTitle = title)
        }.stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = TaskDetailUiState(TaskRepository.find(taskId), editedTitle.value)
        )

    fun onTitleChange(title: String) {
        editedTitle.value = title
    }

    // Task 3.3: the view model asks the repository to rename the task
    fun save() {
        if (editedTitle.value.isNotBlank()) TaskRepository.rename(taskId, editedTitle.value)
    }

    fun toggle() = TaskRepository.toggle(taskId)

    fun delete() = TaskRepository.delete(taskId)

    override fun onCleared() {
        Log.d("ViewModel", "TaskDetailViewModel cleared for task $taskId")
    }
}
